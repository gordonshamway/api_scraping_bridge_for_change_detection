import configparser, os
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv('..\.env')

username = os.getenv('COMPOSER_EMAIL')
password = os.getenv('COMPOSER_PASSWORD')

# css selectors
email_field_selector = 'input[type="email"]'
password_field_selector = 'input[type="password"]'
continue_button_selector = 'button[type="submit"]'
holdings_table_css_selector = 'table[class="table-fixed mt-2 w-full overflow-x-auto"]'
change_line_css_selector = 'div[class="col-span-3"] > span.text-dark-soft'

async def rebuild_into_clean_html_table(html, change_date):
    # rebuild in clean html table
    soup = BeautifulSoup(html, 'html.parser')
    header_tags = soup.select('thead th')
    header_texts = [header.get_text() for header in header_tags]
    header_texts[0] = 'Underlying'
    row_tags = soup.select('tbody tr')
    row_texts = [[cell.get_text() for cell in row.select('td')] for row in row_tags]
    html_table = f"<p>{change_date}</p>\n<table border='1'>\n"
    html_table += "<thead>\n<tr>\n"
    for i in range(0,5):
        html_table += f"<th>{header_texts[i]}</th>\n"
    html_table += "</tr>\n</thead>\n"
    html_table += "<tbody>\n"
    for row_text in row_texts:
        html_table += "<tr>\n"
        for cell_text in row_text:
            if cell_text !='':
                html_table += f"<td>{cell_text}</td>\n"
        html_table += "</tr>\n"
    html_table += "</tbody>\n"

    # Close the HTML table tag
    html_table += "</table>"
    return html_table
    

async def get_website_content(symphony_id):
    symphony_link = f'https://app.composer.trade/symphony/{symphony_id}/details'
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, slow_mo=50)
        page = await browser.new_page()
        await page.goto('https://app.composer.trade/login')
        await page.is_visible(continue_button_selector)
        await page.fill(email_field_selector, username)
        await page.click(continue_button_selector)

        await page.fill(password_field_selector, password)
        await page.click(continue_button_selector)

        await page.goto(symphony_link)
        await page.is_visible(holdings_table_css_selector)

        #wait for 5 seconds until all allocations are loaded
        await page.wait_for_timeout(5000) 
        #extract current holdings
        html = await page.inner_html(holdings_table_css_selector)
        change_date = await page.inner_html(change_line_css_selector)
        clean_html = await rebuild_into_clean_html_table(html, change_date)
        return(clean_html)
    
if __name__ == '__main__':
    website = get_website_content('v9joaHizwHRlN4twG0S8')
    print(website)
