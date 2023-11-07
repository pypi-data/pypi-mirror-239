import pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from gpt4free import you

driver = webdriver.Chrome()
driver.get("https://www.upwork.com/")
driver.maximize_window()


class UpWork:
    def __init__(
        self,
        email,
        password,
        search_input,
        cat_index,
        lev_index,
        prop_index,
        client_index,
        loc_index,
        time_index,
        length_index,
        hour_index,
    ):
        self.email = email
        self.password = password
        self.search_input = search_input
        self.cat_index = cat_index
        self.lev_index = lev_index
        self.prop_index = prop_index
        self.client_index = client_index
        self.loc_index = loc_index
        self.time_index = time_index
        self.length_index = length_index
        self.hour_index = hour_index

    # from web elements list to text elements list
    def w_to_t(self, w_list):
        t_list = []
        for i in range(len(w_list)):
            t_list.append(w_list[i].text)
        return t_list

    def generate_text(self, prompt):
        chat = []
        response = you.Completion.create(prompt=prompt, chat=chat)
        return response.text

    def login_form(self):
        login_link = driver.find_element(By.CLASS_NAME, "login-link")
        login_link.click()
        uname_email_field = driver.find_element(By.ID, "login_username")
        uname_email_field.send_keys(self.email)
        driver.find_element(By.ID, "login_password_continue").click()
        time.sleep(5)
        password_field = driver.find_element(By.ID, "login_password")
        password_field.send_keys(self.password)
        driver.find_element(By.ID, "login_control_continue").click()
        time.sleep(10)

    def search_job(self):
        # load cookies from pkl file

        # get login page

        search_field = driver.find_element(
            By.XPATH, "//*[@id='navSearchForm-desktop']/div[1]/input[2]"
        )
        search_field.send_keys(self.search_input)
        search_field.send_keys(Keys.RETURN)

    def filter_categories(self):
        driver.find_element(
            By.XPATH,
            '//*[@id="main"]/div[2]/div[4]/div/div/div[1]/div/div[2]/div/div[1]/div/div[2]/div/div/div/div/div/input',
        ).click()
        categories = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, "up-menu-checkbox-label")
            )
        )
        categories[self.cat_index].click()
        driver.find_element(
            By.XPATH,
            '//*[@id="main"]/div[2]/div[4]/div/div/div[1]/div/div[1]/h2',
        ).click()

    def filter_levels(self):
        levels = driver.find_elements(
            By.XPATH,
            "//*[@id='main']/div[2]/div[4]/div/div/div[1]/div/div[2]/div/div[2]/div/div[2]/div/fieldset/div/label/span[2]",
        )

        levels[self.lev_index].click()

    def filter_proposals(self):
        proposals = driver.find_elements(
            By.XPATH,
            "//*[@id='main']/div[2]/div[4]/div/div/div[1]/div/div[2]/div/div[4]/div/div[2]/div/fieldset/div/label/span[2]",
        )
        proposals[self.prop_index].click()

    def filter_client_info(self):
        client_info = driver.find_elements(
            By.XPATH,
            "//*[@id='main']/div[2]/div[4]/div/div/div[1]/div/div[2]/div/div[5]/div/div[2]/div/fieldset/div/label/span[2]",
        )
        client_info[self.client_index].click()

    def filter_locations(self):
        driver.find_element(
            By.XPATH,
            "//*[@id='main']/div[2]/div[4]/div/div/div[1]/div/div[2]/div/div[7]/div/div[2]/div/div/div[1]/div/div/input",
        ).click()
        locations = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (
                    By.XPATH,
                    "//*[@id='main']/div[2]/div[4]/div/div/div[1]/div/div[2]/div/div[7]/div/div[2]/div/div/div[2]/div/div[1]/div[1]/div[2]/ul/li/div/label/span[2]",
                )
            )
        )
        locations[self.loc_index].click()
        driver.find_element(
            By.XPATH,
            '//*[@id="main"]/div[2]/div[4]/div/div/div[1]/div/div[1]/h2',
        ).click()

    def filter_times(self):
        driver.find_element(
            By.XPATH,
            "//*[@id='main']/div[2]/div[4]/div/div/div[1]/div/div[2]/div/div[8]/div/div[2]/div/div/div[1]/div/div/input",
        ).click()
        times = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (
                    By.XPATH,
                    "//*[@id='dropdown-menu-null']/li/div/label/span[2]",
                )
            )
        )
        times[self.time_index].click()
        driver.find_element(
            By.XPATH,
            '//*[@id="main"]/div[2]/div[4]/div/div/div[1]/div/div[1]/h2',
        ).click()

    def filter_project_length(self):
        project_length = driver.find_elements(
            By.XPATH,
            "//*[@id='main']/div[2]/div[4]/div/div/div[1]/div/div[2]/div/div[10]/div/div[2]/div/fieldset/div/label/span[2]",
        )
        project_length[self.length_index].click()

    def filter_hours_week(self):
        hours_week = driver.find_elements(
            By.XPATH,
            "//*[@id='main']/div[2]/div[4]/div/div/div[1]/div/div[2]/div/div[11]/div/div[2]/div/fieldset/div/label/span[2]",
        )
        hours_week[self.hour_index].click()

    def fill_text_areas(self):
        text_areas = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, "//textarea"))
        )
        text_areas_titles = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located(
                (
                    By.CLASS_NAME,
                    "label",
                )
            )
        )
        for title in text_areas_titles:
            if title.text == "Attachments":
                text_areas_titles.remove(title)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.CLASS_NAME,
                    "air3-truncation-btn",
                )
            )
        ).click()

        job_description = (
            WebDriverWait(driver, 10)
            .until(EC.presence_of_element_located((By.ID, "air3-truncation-1")))
            .get_attribute("innerHTML")
        )

        x = self.w_to_t(text_areas_titles).index("Cover Letter")
        text_areas_titles = text_areas_titles[x:]
        for i in range(len(text_areas_titles)):
            title = text_areas_titles[i]
            if title.text == "Cover Letter":
                p = "give me a cover letter according to this job description : " + str(
                    job_description
                )
            else:
                p = "give me the best answer to this question :" + str(title.text)
            print(len(text_areas))
            print(len(text_areas_titles))
            print(p)
            text = self.generate_text(p)
            print(text)
            text_areas[i].send_keys(text)


def filter_job_types(h, f, sf):
    hourly = driver.find_element(
        By.XPATH,
        "//*[@id='main']/div[2]/div[4]/div/div/div[1]/div/div[2]/div/div[3]/div/div[2]/div/fieldset/div/label/span[2]",
    )
    fixed = driver.find_element(
        By.XPATH,
        "//*[@id='main']/div[2]/div[4]/div/div/div[1]/div/div[2]/div/div[3]/div/div[2]/div/fieldset/div[3]/div[1]/label/span[2]",
    )
    sub_fixed = driver.find_elements(
        By.XPATH,
        "//*[@id='main']/div[2]/div[4]/div/div/div[1]/div/div[2]/div/div[3]/div/div[2]/div/fieldset/div[3]/div[2]/div/label/span[2]",
    )
    if h and f:
        hourly.click()
        fixed.click()
    elif h:
        hourly.click()
    elif f:
        fixed.click()
        sub_fixed[sf].click()


time.sleep(5)
scrapper = UpWork(
    "oussemabenhassena5@gmail.com", "00000000zero", "ai", 1, 2, 3, 1, 2, 3, 1, 2
)
scrapper.login_form()
time.sleep(5)
cookies = driver.get_cookies()
pickle.dump(cookies, open("cookies.pkl", "wb"))

cookies = pickle.load(open("cookies.pkl", "rb"))

for cookie in cookies:
    driver.add_cookie(cookie)
# time.sleep(10)
# login_link = driver.find_element(By.CLASS_NAME, "login-link")
# login_link.click()
time.sleep(10)
scrapper.search_job()
scrapper.filter_categories()
scrapper.filter_levels()
scrapper.filter_proposals()
scrapper.filter_client_info()
scrapper.filter_locations()
scrapper.filter_times()
scrapper.filter_project_length()
# scrapper.filter_hours_week()
time.sleep(20)
# test
# -----------------submit proposal-----(lack of connects)-----------

# jobs = driver.find_elements(
#     By.CLASS_NAME,
#     "job-tile-title",
# )
# for job in jobs:
#     job.click()
#     apply_btn = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CLASS_NAME, "submit-proposal-button"))
#     )
#     apply_btn.click()
#     parent = driver.window_handles[0]
#     child = driver.window_handles[1]
#     driver.switch_to.window(child)
#     fill_text_areas()
#     description = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CLASS_NAME, "milestone-description"))
#     )
#     description.send_keys("two milestones")
#     description.send_keys(Keys.RETURN)
#     time.sleep(10)
#     amount = driver.find_element(By.XPATH, "//*[@id='milestone-amount-1']")
#     time.sleep(10)
#     amount.send_keys("7")
#     driver.switch_to.window(parent)
# WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located(
#         (
#             By.CLASS_NAME,
#             "air3-btn-primary",
#         )
#     )
# ).click()
# WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located(
#         (
#             By.XPATH,
#             "/html/body/div[8]/div/div[2]/div/div[1]/div[1]/button/div/svg/path",
#         )
#     )
# ).click()
# ---------------------------------------------------------------------
