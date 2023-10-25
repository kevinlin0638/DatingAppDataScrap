import asyncio
from playwright.async_api import async_playwright
import csv
import re

async def process_profile(page, url, is_male):
    profile_data = {
        'gender': 'Female' if not is_male else 'Male',
        'sex': 'Female' if not is_male else 'Male'
    }
    try:
        await page.goto(url, timeout=60000)
        profile_data['profile_url'] = url

        img_url_element = await page.query_selector("div.entry-content > p > a > img")
        if img_url_element:
            profile_data['img_url'] = await img_url_element.get_attribute("src")

        profile_details_element = await page.query_selector("div.entry-content > p")
        if profile_details_element:
            profile_details_text = await profile_details_element.text_content()
            profile_data.update(extract_profile_details(profile_details_text))
    except Exception as e:
        return {}

    return profile_data

def extract_profile_details(text):
    details = {}
    # Define regular expressions for each piece of data
    regex_mappings = {
        'username': re.compile(r'username\s*:\s*(.+)', re.IGNORECASE),
        'email': re.compile(r'email\s*:\s*(.+)', re.IGNORECASE),
        'name': re.compile(r'name\s*:\s*(.+)', re.IGNORECASE),
        'age': re.compile(r'age\s*:\s*(\d+)', re.IGNORECASE),
        'location': re.compile(r'location\s*:\s*(.+)', re.IGNORECASE),
        'marital_status': re.compile(r'marital status\s*:\s*(.+)', re.IGNORECASE),
        'children': re.compile(r'children\s*:\s*(.+)', re.IGNORECASE),
        'sexual_orientation': re.compile(r'sexual orientation\s*:\s*(.+)', re.IGNORECASE),
        'ethnicity': re.compile(r'ethnicity\s*:\s*(.+)', re.IGNORECASE),
        'religion': re.compile(r'religion\s*:\s*(.+)', re.IGNORECASE),
        'occupation': re.compile(r'occupation\s*:\s*(.+)', re.IGNORECASE),
        'description': re.compile(r'description\s*:\s*(.+)', re.DOTALL | re.IGNORECASE)
    }

    for key, regex in regex_mappings.items():
        match = regex.search(text)
        if match:
            details[key] = match.group(1).strip()

    return details


async def process_page(page_number, context, is_male):
    url = f'https://scamdigger.com/category/male-profiles/page/{page_number}/' if is_male else f'https://scamdigger.com/category/female-profiles/page/{page_number}/'
    page = await context.new_page()
    await page.goto(url, timeout=600000)
    profile_urls_elements = await page.query_selector_all('h1.entry-title > a')
    profile_urls = [await element.get_attribute('href') for element in profile_urls_elements]

    profiles_data = []
    for profile_url in profile_urls:
        profile_data = await process_profile(page, profile_url, is_male)
        if 'profile_url' in profile_data:
            profiles_data.append(profile_data)

    await page.close()

    return profiles_data

async def save_to_csv(data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = [
            'profile_url',
            'img_url',
            'username',
            'email',
            'name',
            'age',
            'looking_for',
            'gender',
            'match_age',
            'location',
            'marital_status',
            'children',
            'sexual_orientation',
            'ethnicity',
            'religion',
            'occupation',
            'description',
            'here_for',
            'last_activity',
            'smoke',
            'drink',
            'sex'
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

async def main(is_male):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        start = 1
        end = 144
        concurrent_tasks = 5
        all_data = []
        for i in range(start, end + 1, concurrent_tasks):
            tasks = [process_page(page_number, context, is_male) for page_number in range(i, min(i + concurrent_tasks, end + 1))]
            results = await asyncio.gather(*tasks)
            all_data.extend(sum(results, []))
        await save_to_csv(all_data, 'spam_output_male.csv' if is_male else'spam_output_female.csv')
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main(True))
    asyncio.run(main(False))
