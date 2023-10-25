import asyncio
import csv
from playwright.async_api import async_playwright


async def extract_user_data(url, playwright):
    page = await playwright.new_page()

    data = {}
    try:
        # Extracting basic information
        await page.goto(url, timeout=600000)
        basic_info_elements = await page.query_selector_all('.section_f90cde5913235d172603cc4e7b9726e3 .ow_value span')
        basic_info_labels = ['username', 'gender', 'age', 'here_for', 'looking_for', 'match_age']
        for elem, label in zip(basic_info_elements, basic_info_labels):
            data[label] = await elem.text_content()

        # Extracting location
        location_elem = await page.query_selector('.section_69d3e58e0b1bd9ada5172f8b650a715b .ow_value span a')
        if location_elem:
            data['location'] = await location_elem.text_content()

        # Extracting more info
        more_info_elements = await page.query_selector_all('.section_1c39c2d13da6947108873e2896c31c51 .ow_value span')
        more_info_labels = ['marital_status', 'children', 'sexual_orientation', 'ethnicity', 'religion', 'smoke', 'drink',
                            'occupation']
        for elem, label in zip(more_info_elements, more_info_labels):
            data[label] = await elem.text_content()

        # Extracting description
        description_elem = await page.query_selector('.section_683bffc1ac46b8bd0c840a3526cce25b .ow_value span')
        if description_elem:
            data['description'] = await description_elem.text_content()

        print(f'Extracted basic information for {data["username"]}')
    except Exception as e:
        await page.close()
        print(e)
        return None

    await page.close()
    return data


async def process_batch(urls, playwright):
    tasks = [extract_user_data(url, playwright) for url in urls]
    return await asyncio.gather(*tasks)


async def update_csv(input_filename, output_filename, playwright):
    with open(input_filename, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    new_data = []
    for i in range(0, len(rows), 8):  # Process in batches of 5
        batch_urls = [row['profile_url'] for row in rows[i:i + 5]]
        batch_data = await process_batch(batch_urls, playwright)

        for row, user_data in zip(rows[i:i + 5], batch_data):
            if user_data is None:
                continue
            updated_row = {**row, **user_data}
            new_data.append(updated_row)

    fieldnames = rows[0].keys() | ['username', 'gender', 'age', 'here_for', 'looking_for', 'match_age', 'location',
                                   'marital_status', 'children', 'sexual_orientation', 'ethnicity', 'religion', 'smoke',
                                   'drink', 'occupation',
                                   'description']  # Union of keys from both dicts
    with open(output_filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(new_data)


async def main():
    input_filename = 'output.csv'  # Your existing CSV file
    output_filename = 'data.csv'  # New CSV file with additional data
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context()
        await update_csv(input_filename, output_filename, context)


if __name__ == '__main__':
    asyncio.run(main())
