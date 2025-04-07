import requests

def send_results_to_springboot(result_dict: dict):
    url = "http://localhost:8081/api/files/upload_result"
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, json=result_dict, headers=headers)
        if response.status_code == 200:
            print("✅ SpringBoot에 성공적으로 전송됨")
        else:
            print(f"❌ SpringBoot 전송 실패: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ SpringBoot 통신 오류: {str(e)}")