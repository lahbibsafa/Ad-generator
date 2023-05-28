import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def authenticate(driver, username, password):
    driver.get("https://www.facebook.com/")
    username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
    password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pass")))
    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "login")))
    login_button.click()

def extract_food_posts(driver, page_url):
    driver.get(page_url)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "userContentWrapper")))
    posts = driver.find_elements_by_class_name("userContentWrapper")
    data = []
    for post in posts:
        post_text = post.text
        reactions = post.find_element_by_css_selector("._4arz")
        likes = reactions.get_attribute("aria-label")
        comments = post.find_element_by_css_selector("._4arz._12qz._pq2")
        comments_count = comments.get_attribute("aria-label")
        data.append([post_text, likes, comments_count])
    return data

def save_to_csv(data, filename):
    with open(filename, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Post", "Likes", "Comments"])
        writer.writerows(data)

def main():
    username = "farahlamine306@gmail.com"
    password = "azerty098@"
    page_url = "https://www.facebook.com/Dominos/"
    driver = webdriver.Chrome("/usr/bin/chromedriver ")

    authenticate(driver, username, password)
    data = extract_food_posts(driver, page_url)
    save_to_csv(data, "food_posts.csv")

    driver.quit()

if __name__ == "__main__":
    main()
