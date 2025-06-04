import asyncio
from urllib.parse import quote
from playwright.async_api import async_playwright

async def get_valorant_stats(username):
    encoded_username = quote(username)
    url = f"https://tracker.gg/valorant/profile/riot/{encoded_username}/overview"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, timeout=60000)

        try:
            await page.wait_for_selector("div.trn-match-row", timeout=20000)
            match = await page.query_selector("div.trn-match-row")

            agent = await match.query_selector("div.vmr-agent img")
            map_name = await match.query_selector("div.vmr-metadata div.trn-match-row__text-value")
            result_class = await match.get_attribute("class")
            score = await match.query_selector("div.vmr-score .trn-match-row__text-value")
            kda = await match.query_selector("xpath=.//div[.='K / D / A']/following-sibling::div")
            kd_ratio = await match.query_selector("xpath=.//div[.='K/D']/following-sibling::div")
            adr = await match.query_selector("xpath=.//div[.='ADR']/following-sibling::div")
            acs = await match.query_selector("xpath=.//div[.='ACS']/following-sibling::div")
            hs_percent = await match.query_selector("xpath=.//div[.='HS%']/following-sibling::div")

            return {
                "agent": await agent.get_attribute("alt") if agent else None,
                "map": await map_name.text_content() if map_name else None,
                "result": "Loss" if "trn-match-row--outcome-loss" in result_class else "Win",
                "score": await score.text_content() if score else None,
                "kda": await kda.text_content() if kda else None,
                "kd_ratio": await kd_ratio.text_content() if kd_ratio else None,
                "adr": await adr.text_content() if adr else None,
                "acs": await acs.text_content() if acs else None,
                "hs_percent": await hs_percent.text_content() if hs_percent else None,
            }
        finally:
            await browser.close()

if __name__ == "__main__":
    username = input("Enter Riot username (e.g. birjuan#69420): ")
    data = asyncio.run(get_valorant_stats(username))
    print(data)
