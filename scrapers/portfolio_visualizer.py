import configparser, os
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv('..\.env')

username = os.getenv('PV_EMAIL')
password = os.getenv('PV_PASSWORD')
timeout = os.getenv('PV_TIMEOUT_SECONDS')

# css selectors
email_field_selector = '#username'
password_field_selector = '#password'
submit_button_selector = '#submitButton'
model_trades_selector = 'button#timingPeriods_btn'
trade_signal_selector = '#timingPeriods > div:nth-child(5) > div.card-body > table'


async def rebuild_into_clean_html_table(html, name):
    # rebuild in clean html table
    soup = BeautifulSoup(html, 'html.parser')

    header_tags = soup.select('thead th')
    header_texts = [header.get_text() for header in header_tags]
    row_tags = soup.select('tbody tr')
    row_texts = [[cell.get_text() for cell in row.select('td')] for row in row_tags]
    html_table = f"<table border='1'>\n"
    html_table += f"<p>{name}</p>\n<thead>\n<tr>\n"
    for i in range(len(header_texts)):
        html_table += f"<th>{header_texts[i]}</th>\n"
    html_table += "</tr>\n</thead>\n"
    html_table += "<tbody>\n"
    for row_text in row_texts[:5]:
        html_table += "<tr>\n"
        for cell_text in row_text:
            if cell_text !='':
                html_table += f"<td>{cell_text}</td>\n"
        html_table += "</tr>\n"
    html_table += "</tbody>\n"

    # Close the HTML table tag
    html_table += "</table>"
    return html_table

async def get_pv_content(link, name):
    login_link = f'https://www.portfoliovisualizer.com/login'
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=50)
        page = await browser.new_page()
        #login in
        await page.goto(login_link)
        await page.is_visible(submit_button_selector)
        await page.fill(email_field_selector, username)
        await page.fill(password_field_selector, password)
        await page.click(submit_button_selector)

        # wait to load page while finding the "Run Test"
        await page.goto(link)
        await page.wait_for_timeout(5 * 1000)
        await page.is_visible(submit_button_selector)
        await page.click(submit_button_selector)
        await page.wait_for_timeout(int(timeout) * 1000)
        html = await page.inner_html(trade_signal_selector)
        result = await rebuild_into_clean_html_table(html, name)
        return result


if __name__ == '__main__':
    content = get_pv_content('https://www.portfoliovisualizer.com/tactical-asset-allocation-model?s=y&sl=4SIEYLD28O2OX0YHBOopRA', 'P3-weekly')
    print(content)