import asyncio
import csv

from playwright.async_api import async_playwright


async def process_page(page_number, pwc):
    data = []
    page = await pwc.new_page()
    try:
        await page.goto(f'https://datingnmore.com/site/users?&page={page_number}')
        ppl = await page.query_selector_all('.ow_user_list_item')

        for person in ppl:
            person_data = {}
            person_data['name'] = await person.eval_on_selector('.ow_user_list_data a', 'a => a.textContent')
            person_data['profile_url'] = await person.eval_on_selector('.ow_user_list_data a', 'a => a.href')
            person_data['img_url'] = await person.eval_on_selector('.ow_user_list_picture img', 'img => img.src')

            sex_age_text = await person.eval_on_selector('.ow_user_list_data .ow_small', 'div => div.textContent')
            sex_age_lines = sex_age_text.strip().split('\n')
            if len(sex_age_lines[0].split()) == 2:
                sex, age = sex_age_lines[0].split()
                person_data['sex'] = sex
                person_data['age'] = int(age)

            if len(sex_age_lines) > 1:
                remark_text = sex_age_lines[1].split(': ')[1]
                person_data['last_activity'] = remark_text

            data.append(person_data)
    except Exception as e:
        print(e)
    await page.close()
    print(f'Processed {page_number}')
    return data


async def save_to_csv(data, filename):
    fieldnames = ['name', 'sex', 'age', 'img_url', 'last_activity', 'profile_url']
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        start = 1
        end = 3363
        concurrent_tasks = 5  # Number of concurrent pages to process
        all_data = []
        # await process_page(1, context)
        for i in range(start, end + 1, concurrent_tasks):
            tasks = [process_page(page_number, context) for page_number in range(i, min(i + concurrent_tasks, end + 1))]
            results = await asyncio.gather(*tasks)
            all_data.extend(sum(results, []))  # Flatten the list of lists and extend all_data

        await save_to_csv(all_data, 'output.csv')
        await browser.close()


if __name__ == '__main__':
    asyncio.run(main())
