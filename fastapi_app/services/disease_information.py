import selenium
import re
import time
import cx_Oracle
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ✅ Oracle DB 연결
dsn = cx_Oracle.makedsn("localhost", 1521, service_name="xepdb1")
conn = cx_Oracle.connect(user="TESTAPP", password="TESTAPP", dsn=dsn)
cursor = conn.cursor()

# ✅ Selenium 크롬 드라이버 설정
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=service, options=options)
print("✅ 드라이버 실행됨")

driver.get("https://health.kdca.go.kr/healthinfo/")
time.sleep(2)

# ✅ 건강정보 버튼 클릭
try:
    health_info_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '건강정보')]"))
    )
    health_info_button.click()
    print("✅ 건강정보 버튼 클릭됨")
except Exception as e:
    print("❌ 건강정보 버튼을 찾을 수 없음:", e)

# ✅ 카테고리 반복
for i in range(1, 15):
    try:
        xpath = f"/html/body/div[6]/div[1]/div[2]/div[2]/form/div[2]/div[2]/div/a[{i}]"
        category_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        category_name = category_button.text.strip()
        category_button.click()
        print(f"✅ {category_name} 카테고리 클릭됨")

        # ✅ 소주제 반복
        for j in range(1, 13):
            try:
                sub_xpath = f"#gnrlzHealthInfoMainForm > div.hd-indexbox > ul > li:nth-child({j}) > a"
                sub_category_button = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, sub_xpath))
                )

                if not sub_category_button.is_displayed():
                    raise Exception("소주제가 비활성화됨")

                sub_category_name = sub_category_button.text.strip()
                sanitized_name = re.sub(r'[\\/*?:"<>|]', "", sub_category_name)
                sub_category_button.click()
                print(f"✅ {sub_category_name} 클릭됨 ({category_name} 내)")

                try:
                    print_content = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#print-content"))
                    )
                    html_content = print_content.get_attribute("outerHTML")

                    # ✅ Oracle DB 저장
                    cursor.execute(
                        "INSERT INTO disease_information (category, subcategory, html_content) VALUES (:1, :2, :3)",
                        (category_name, sub_category_name, html_content)
                    )
                    conn.commit()
                    print(f"✅ {sub_category_name} DB 저장 완료!")

                except Exception as e:
                    print(f"❌ {sub_category_name} HTML 크롤링 실패:", e)

                driver.back()
                time.sleep(2)

            except Exception:
                print(f"⚠️ {category_name} 내 {j}번째 소주제가 존재하지 않음. 다음 카테고리로 이동.")
                break

        driver.back()
        time.sleep(2)

    except Exception as e:
        print(f"❌ a[{i}] 카테고리를 찾을 수 없음:", e)

driver.quit()
cursor.close()
conn.close()
print("✅ 브라우저 종료 + DB 연결 종료")
