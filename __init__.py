from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException
import csv

# Set up Selenium and open the website
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://talentedge.com/browse-courses")

# Wait for the course listings to load
wait = WebDriverWait(driver, 10)
courses = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'course-card')))

# Initialize a list to store the course data
course_data = []
faculty_names = []

# Loop through the courses and extract data
for i in range(10):  # Limiting to the first 10 courses
    try:
        course = courses[i]  # Get the course element

        # Extract the course title
        title_element = course.find_element(By.CLASS_NAME, 'courses-name')
        title = title_element.text

        # Extract the course link
        link_element = title_element.find_element(By.TAG_NAME, 'a')
        link = link_element.get_attribute('href')

        # Extract the description (e.g., Doctorate)
        description_element = course.find_element(By.CLASS_NAME, 'looking-for')
        description = description_element.text

        # Extract the duration, timing, and start date
        details = course.find_elements(By.CSS_SELECTOR, '.course-specification ul li')

        # Safely get the duration, timing, and start date
        duration = details[1].text if len(details) > 1 else 'N/A'
        timing = details[2].text if len(details) > 2 else 'N/A'
        start_date = details[3].text if len(details) > 3 else 'N/A'

        # Extract the course fee
        fee_element = course.find_element(By.CLASS_NAME, 'course-price-div')
        fee = fee_element.text

        # Navigate to the course detail page to extract additional information
        driver.get(link)

        try:
            # Extract the eligibility information
            eligibility_element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.eligible-right-inner p')))
            eligibility = eligibility_element.text
        except:
            eligibility = 'Graduates (10+2+3) or Diploma Holders (only 10+2+3) from a recognized university (UGC/AICTE/DEC/AIU/State Government)'

        try:
            # Try to find the faculty name using the initial CSS selector
            faculty_name_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.best-fname')))
            faculty_name = faculty_name_element.text
        except (TimeoutException, NoSuchElementException):
            print("Faculty name not found using .best-fname, trying h4 tag...")
            try:
                # If not found, try to find it using the h4 tag
                faculty_name_element = wait.until(
                    EC.presence_of_element_located((By.XPATH, '//div[@class="el-fec-right"]//h4')))
                faculty_name = faculty_name_element.text
            except (TimeoutException, NoSuchElementException):
                print("Faculty name not found in h4 tag either.")

        faculty_names.append(faculty_name)
        print(f"Extracted Faculty Name: {faculty_name}")  # Debugging line

        try:
            # Extract the university name
            university_name_element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a.text-decoration-none')))
            university_name = university_name_element.text
            print(f"Extracted University Name: {university_name}")  # Debugging line for successful extraction
        except Exception as e:
            university_name = 'CORNELL UNIVERSITY'
            print(f"Failed to extract university name.")  # Debugging line for failure

        # Extract the skills from the ul/li tags
        try:
            skills_elements = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.key-skills-sec ul li')))
            skills = [skill.text for skill in skills_elements if skill.text]
            skills_text = ', '.join(skills)
            if not skills_text:  # If skills_text is empty
                raise Exception("No skills found in key-skills-sec ul/li.")
            print(f"Extracted Skills: {skills_text}")  # Debugging line for successful extraction
        except Exception as e:
            print(f"Failed to extract skills from ul/li. Attempting to extract from div/strong...")
            try:
                # Attempt to scrape the skills from div/strong tags
                skills_elements = wait.until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.el-lap-h-r strong')))
                skills = [skill.text for skill in skills_elements if skill.text]
                skills_text = ', '.join(skills)
                print(f"Extracted Skills from div/strong: {skills_text}")  # Debugging line for successful extraction
            except Exception as e:
                skills_text = 'N/A'
                print(f"Failed to extract skills from div/strong.")  # Debugging line for failure

        # Go back to the course listing page
        driver.back()

        # Re-fetch the list of courses to avoid stale elements
        courses = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'course-card')))

        # Append the extracted data to the list
        course_data.append({
            "Title": title,
            "Link": link,
            "Description": description,
            "Duration": duration,
            "Timing": timing,
            "Start Date": start_date,
            "Fee": fee,
            "Eligibility": eligibility,
            "Faculty Name": faculty_name,
            "University Name": university_name,
            "Skills": skills_text
        })

    except StaleElementReferenceException:
        print(f"Encountered a stale element reference for course index {i}. Retrying...")
        # Re-fetch the list of courses and retry the current index
        courses = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'course-card')))
        continue

# Write the data to a CSV file
with open('courses_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Title', 'Link', 'Description', 'Duration', 'Timing', 'Start Date', 'Fee',
                                              'Eligibility', 'Faculty Name', 'University Name', 'Skills'])
    writer.writeheader()
    writer.writerows(course_data)

print("Data has been written to courses_data.csv")

# Quit the driver
driver.quit()
