import asyncio
import pandas as pd
from playwright.async_api import async_playwright

from spam.spam_digger import process_profile


async def process_profiles_concurrently(context, urls, is_male):
    tasks = []
    for url in urls:
        page = await context.new_page()
        tasks.append(process_profile(page, url, is_male))
    results = await asyncio.gather(*tasks)
    for page in context.pages:
        await page.close()
    return results


async def update_missing_usernames(file_path, is_male):
    df = pd.read_csv(file_path)
    missing_urls = df[df['username'].isnull()]['profile_url'].tolist()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        # Process 5 URLs concurrently
        for i in range(0, len(missing_urls), 5):
            chunk = missing_urls[i:i + 5]
            results = await process_profiles_concurrently(context, chunk, is_male)
            for profile_data in results:
                if 'profile_url' in profile_data and 'username' in profile_data:
                    index = df[df['profile_url'] == profile_data['profile_url']].index[0]
                    for key, value in profile_data.items():
                        df.at[index, key] = value
                    print(f"Username {profile_data['username']} has been filled.")

        await browser.close()

    # Count rows where username is still null
    missing_count = df['username'].isnull().sum()

    # Print the count
    print(f"There are {missing_count} rows where the username is still null.")

    df.to_csv(file_path + '_updated', index=False)


async def run_update_manually(url):

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        page = await context.new_page()
        result = await process_profile(page, url, False)
        print(result.items())

        await page.close()
        await browser.close()

if __name__ == '__main__':
    asyncio.run(update_missing_usernames('spam_output_female.csv'), False)
    asyncio.run(update_missing_usernames('spam_output_male.csv', True))
    # asyncio.run(run_update_manually('https://scamdigger.com/2012/08/jeremy-klarkson-jeremyklarksonyahoo-com/'))