import asyncio
import csv
from playwright.async_api import async_playwright


async def extract_user_data(url, playwright):
    page = await playwright.new_page()

    # Initialize the data dictionary with the user's URL
    data = {'user_url': url, 'friends': []}
    try:
        # Extracting basic information
        await page.goto(url, timeout=600000)

        # Query all elements that contain friend information
        friend_elements = await page.query_selector_all('.ow_lp_avatars .ow_lp_avatars .ow_avatar a')

        # Extract friends' URLs and usernames
        for friend_element in friend_elements:
            friend_url = await friend_element.get_attribute('href')
            friend_username = friend_url.split('/')[-1]
            if friend_url and friend_username:
                data['friends'].append({
                    'friend_username': friend_username,
                    'friend_url': friend_url
                })

        print(f'Extracted friends information for {url}')
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

    # Define fieldnames for the output CSV file
    fieldnames = ['user_url', 'username', 'friend_username', 'friend_url']

    # Open the output CSV file for writing
    with open(output_filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        # Process rows in batches
        for i in range(0, len(rows), 5):  # Adjust batch size as needed
            batch_urls = [row['profile_url'] for row in rows[i:i + 5]]
            batch_data = await process_batch(batch_urls, playwright)

            # Iterate over each user and their friends
            for row, user_data in zip(rows[i:i + 5], batch_data):
                if user_data is None:
                    continue

                if len(user_data['friends']) == 0:
                    continue

                # Create a new row for each friend
                for friend in user_data['friends']:
                    new_row = {
                        'user_url': row['profile_url'],
                        'username': row['name'],
                        'friend_username': friend['friend_username'],
                        'friend_url': friend['friend_url']
                    }
                    writer.writerow(new_row)


async def main():
    input_filename = '../../scrap/normal/output.csv'  # Your existing CSV file
    output_filename = 'user_friends.csv'  # New CSV file with additional data
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context()
        await update_csv(input_filename, output_filename, context)


if __name__ == '__main__':
    asyncio.run(main())
