import pandas as pd
from playwright.sync_api import sync_playwright

def crawl():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        url = 'https://taxlaw.nts.go.kr/qt/USEQTJ001M.do'
        page.goto(url)
        page.wait_for_timeout(3000)

        containers = page.locator('.substance_wrap')
        count = containers.count()
        print(f'총 {count}개의 항목 중 상위 10개만 수집합니다.')

        data_list = []

        for idx in range(min(10, count)):
            try:
                container = containers.nth(idx)
                title = container.locator('.subs_title strong').inner_text()
                doc_number = container.locator('.subs_detail li').nth(0).inner_text()
                prod_date = container.locator('.subs_detail li').nth(1).inner_text()

                summary_elements = container.locator('.subs_text p')
                summary_count = summary_elements.count()
                summary_text = "\n".join([summary_elements.nth(i).inner_text() for i in range(summary_count)])

                with context.expect_page() as new_page_info:
                    container.locator('.subs_title').click()
                new_page = new_page_info.value
                new_page.wait_for_load_state()

                try:
                    new_page.wait_for_selector('.bo_body', timeout=5000)

                    def get_text(selector):
                        elements = new_page.locator(selector)
                        return "\n".join([elements.nth(i).inner_text() for i in range(elements.count())])

                    gist_text = get_text('div.word_group[data-center-type="body_content_gist"] p')
                    reply_text = get_text('div.word_group[data-center-type="body_content_cntn"] p')
                    detail_text = get_text('div#cntnWrap_html p')

                    full_text = f"[요지]\n{gist_text}\n\n[회신]\n{reply_text}\n\n[상세내용]\n{detail_text}"
                except:
                    full_text = '본문 로딩 실패'

                new_page.close()

                data_list.append({
                    '제목': title,
                    '문서정보': doc_number,
                    '생산일자': prod_date,
                    '요약내용': summary_text,
                    '상세본문': full_text
                })

                print(f'[{idx+1}] {title} ✅ 수집 완료')

            except Exception as e:
                print(f'[{idx+1}] ❌ 수집 실패: {e}')
                continue

        df = pd.DataFrame(data_list)
        df.to_json('세법_질의회신_상세본문_playwright.json', orient='records', indent=2, force_ascii=False)
        print("✅ JSON 저장 완료: 세법_질의회신_상세본문_playwright.json")

        browser.close()
