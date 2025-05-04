from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

chrome_options = Options()
chrome_options.add_argument("--headless")  # GUI 없이 실행
chrome_options.add_argument("--no-sandbox")  # Render 환경에 필요
chrome_options.add_argument("--disable-dev-shm-usage")  # 메모리 문제 방지

driver = webdriver.Chrome(options=chrome_options)
url = 'https://taxlaw.nts.go.kr/qt/USEQTJ001M.do'
driver.get(url)
time.sleep(3)

main_window = driver.current_window_handle
containers = driver.find_elements(By.CLASS_NAME, 'substance_wrap')
print(f'총 {len(containers)}개 항목 중 상위 10개만 수집합니다.')

limit = 10
containers = containers[:limit]

data_list = []

for idx, container in enumerate(containers):
    try:
        link_elem = container.find_element(By.CLASS_NAME, 'subs_title')
        title_text = link_elem.find_element(By.TAG_NAME, 'strong').text.strip()

        doc_info = container.find_elements(By.CLASS_NAME, 'subs_detail')[0].find_elements(By.TAG_NAME, 'li')
        doc_number = doc_info[0].text.strip()
        prod_date = doc_info[1].text.strip()

        paragraphs = container.find_element(By.CLASS_NAME, 'subs_text').find_elements(By.TAG_NAME, 'p')
        summary_text = '\n'.join([p.text.strip() for p in paragraphs])

        # 클릭하여 새 창 열기
        link_elem.click()

        # 새 창 전환
        all_windows = driver.window_handles
        for handle in all_windows:
            if handle != main_window:
                driver.switch_to.window(handle)
                break

        # 상세 본문 수집
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'bo_body'))
            )

            # 요지
            try:
                gist_paragraphs = driver.find_elements(By.CSS_SELECTOR, 'div.word_group[data-center-type="body_content_gist"] p')
                gist_text = '\n'.join([p.text.strip() for p in gist_paragraphs])
            except:
                gist_text = ''

            # 회신
            try:
                reply_paragraphs = driver.find_elements(By.CSS_SELECTOR, 'div.word_group[data-center-type="body_content_cntn"] p')
                reply_text = '\n'.join([p.text.strip() for p in reply_paragraphs])
            except:
                reply_text = ''

            # 상세내용
            try:
                detail_paragraphs = driver.find_elements(By.CSS_SELECTOR, 'div#cntnWrap_html p')
                detail_text = '\n'.join([p.text.strip() for p in detail_paragraphs])
            except:
                detail_text = ''

            detail_content = f"[요지]\n{gist_text}\n\n[회신]\n{reply_text}\n\n[상세내용]\n{detail_text}"

        except:
            detail_content = '본문 로딩 실패'

        # 창 닫고 복귀
        driver.close()
        driver.switch_to.window(main_window)

        # 저장
        data_list.append({
            '제목': title_text,
            '문서정보': doc_number,
            '생산일자': prod_date,
            '요약내용': summary_text,
            '상세본문': detail_content
        })

        print(f'[{idx+1}] {title_text} ✅ 본문 수집 완료')

    except Exception as e:
        print(f'[{idx+1}] ❌ 수집 실패: {e}')
        continue

# JSON 저장
df = pd.DataFrame(data_list)
df.to_json('세법_질의회신_상세본문.json', force_ascii=False, orient='records', indent=2)
print("✅ JSON 저장 완료: 세법_질의회신_상세본문.json")

driver.quit()
