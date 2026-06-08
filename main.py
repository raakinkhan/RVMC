#  RV MARKS CHECKER



# What problem it solves?
# it checks the marks of other students as quick as possible which will help reduce time to
# check manually and also reduce the human error in checking
# this code is specially built for me to check rank and instantly know if I am getting achiever's card or not

import re
from playwright.sync_api import sync_playwright
import Reader


with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome", headless=False)
    page = browser.new_page()
    student_data = Reader.Read()

    def get_indiviual(username, exam_type="kcet", exam_name="II PU WEEKLY TEST 09 (KCET 03)"):
        def dashboard_entering():
            jm2 = page.locator(".card-body").filter(
                has_text="Course Code : 2JM"
            ).filter(has_text="Active")
            jm2.click()

            page.wait_for_timeout(1000)
            #  why 2 times? i checked that the website has one rare bug, it throws u back to the same page twice
            jm2 = page.locator(".card-body").filter(
                has_text="Course Code : 2JM"
            ).filter(has_text="Active")
            if jm2.is_visible():
                jm2.click()

            page.get_by_text("Test Performance", exact=True).click()

            if exam_type == "kcet":
                kcet = page.get_by_role("heading", name="KCET")
                page.wait_for_timeout(1000)
                if kcet.is_visible():
                    kcet.click()
                else:
                    print("can't find kcet")
            else:
                jee = page.get_by_role("heading", name="JEE Main")
                page.wait_for_timeout(1000)
                if jee.is_visible():
                    jee.click()
                else:
                    print("can't find jee")

            exam_obj = page.get_by_role("heading", name=exam_name)
            page.wait_for_timeout(2000)
            if exam_obj.is_visible():
                exam_obj.click()
                individual = username
                marks = page.locator('//*[@id="main-content"]/div/div/div[3]/main/div[2]/div/div[2]/span[1]').text_content()
                # return (individual, marks) ###
                print(student_data[int(individual)][0], marks, )
                page.wait_for_timeout(1000)

            else:
                print("Marks not published")

        def login_page_entering(username, parents=False):
            password = username
            if parents:
                username += "_p"


            page.get_by_placeholder("Username").fill(username)
            # password input
            page.get_by_placeholder("Password").fill(password)
            # click login button
            page.get_by_role("button", name="LOGIN").click()


        page.goto("https://rvlh.ilearn.edusquares.com/login")
        login_page_entering(parents=False, username=username)
        page.wait_for_timeout(2000)

        if page.get_by_text("Incorrect User Name or").is_visible() is False:
            dashboard_entering()

        else:
            print("password changed")
            login_page_entering(parents=True, username=username)
            page.wait_for_timeout(1000)
            dashboard_entering()
            page.wait_for_timeout(1000)

            if page.get_by_text("Incorrect User Name or").is_visible():
                print("The person has changed both account password")
            else:
                dashboard_entering()


    for _, idx in enumerate(student_data):
        get_indiviual(username=str(idx), exam_type="jee", exam_name="II PU WEEKLY TEST 10 (JEE MAIN)")
        # if _ >= 11:
        #     get_indiviual(username=str(idx))
    # get_indiviual(username="250885")



