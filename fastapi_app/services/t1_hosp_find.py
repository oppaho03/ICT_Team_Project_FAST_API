import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import os
import cx_Oracle  # ✅ DB 저장용 추가

def scroll_down(driver):
    """
    스크롤을 최하단까지 내려서 더 많은 병원 데이터를 불러오는 함수
    """
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def hira_health():
    try:
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")

        driver = webdriver.Chrome(service=service, options=options)
        driver.get(
            "https://www.hira.or.kr/ra/hosp/getHealthMap.do?tabgbn=03&WT.ac=HIRA%EA%B1%B4%EA%B0%95%EC%A7%80%EB%B0%94%EB%A1%9C%EA%B0%80%EA%B8%B0#")
        print("🌍 웹사이트 접속 완료")

        region = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="hosp-form"]/div[2]/a')))
        driver.execute_script("arguments[0].click();", region)
        print("✅ 지역 선택 클릭 성공")

        seoul = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="sidoCdMap"]/li[2]/a')))
        driver.execute_script("arguments[0].click();", seoul)
        print("✅ 서울 선택 클릭 성공")

        confirm_button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, "btnSearchJuso")))
        driver.execute_script("arguments[0].click();", confirm_button)
        print("✅ 확인 버튼 클릭 성공")

        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#resultLayer2 div ul li")))
        print("📋 병원 목록 로드 성공")

        scroll_down(driver)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        li_tags = soup.select("#resultLayer2 div ul li")

        print(f"🔍 크롤링된 병원 개수: {len(li_tags)}")

        hospitals = []

        for li in li_tags:
            name_tag = li.select_one("a.tit")
            address_tag = li.select_one("p span:nth-of-type(6)")
            distance_tag = li.select_one("span")

            if name_tag and distance_tag:
                name = name_tag.get_text(strip=True)
                address = address_tag.get_text(strip=True) if address_tag else "주소 없음"
                distance = distance_tag.get_text(strip=True).replace("주소", "").strip()

                hospitals.append({"name": name, "address": address, "distance": distance})

        print(f"🏥 추출된 병원 정보 수: {len(hospitals)}")

        if not hospitals:
            print("⚠️ 병원 정보를 추출하지 못했습니다. HTML 구조가 변경되었을 수 있습니다.")

        save_dir = os.path.expanduser("./")
        json_path = os.path.join(save_dir, "hira_health_seoul.json")

        with open(json_path, "w", encoding="utf8") as f:
            json.dump(hospitals, f, indent=4, ensure_ascii=False)

        print(f"\n💾 JSON 저장 완료: {json_path}")

        # ✅ Oracle DB 저장
        dsn = cx_Oracle.makedsn("localhost", 1521, service_name="xepdb1")
        conn = cx_Oracle.connect(user="TESTAPP", password="TESTAPP", dsn=dsn)
        cursor = conn.cursor()

        for hospital in hospitals:
            try:
                cursor.execute(
                    "INSERT INTO hira_hospital_info (name, address, distance) VALUES (:1, :2, :3)",
                    (hospital["name"], hospital["address"], hospital["distance"])
                )
                conn.commit()
                print(f"✅ DB 저장 완료: {hospital['name']}")
            except Exception as e:
                print(f"❌ DB 저장 실패: {hospital['name']} - {e}")

        cursor.close()
        conn.close()
        print("✅ DB 연결 종료")

    except TimeoutException as e:
        print("⏳ 요소를 찾을 수 없습니다:", e)
    except ElementNotInteractableException as e:
        print("⚠️ 요소와 상호작용할 수 없습니다:", e)
    finally:
        driver.quit()
        print("\n✅ 크롤링 작업 완료. 프로그램 종료.\n")


if __name__ == "__main__":
    hira_health()
