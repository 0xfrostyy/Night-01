import asyncio
from playwright.async_api import async_playwright, TimeoutError

ANSWER = "C"

accounts = [
    {"username":"sunny-1","wallet":"3HBrdGigUxi3FokCeV6VsY46E744GMgVJPZhg13NyfYf"},
    {"username":"sunny-2","wallet":"GEVGkbE4v5vzNXoc1Fid2mBm6oCKq3mxQbE3w9HbfAEK"},
    {"username":"sunny-3","wallet":"GpNNbBBLgoPaNNj6V5cWBFUhX43jjdE53VJijvPhFhsu"},
    {"username":"sunny-4","wallet":"5cdLqMUwy5okG4aTBwsY6F2uFzSnjfRs3iY8GCrbJ9AT"},
    {"username":"sunny-5","wallet":"DRZDT6rW5bZXvJFKrp31bkkS8RxMfx8ktXD381AnyeUq"},
    {"username":"sunny-6","wallet":"CfjMTYs6A2MbDiokKBc5CWq8jbcy8iea7tsfw9D6N8Do"},
    {"username":"sunny-7","wallet":"DB8r45ai2EgnuxKf13JqbpxrLPxxBF2eJACopC6Er1aH"},
    {"username":"sunny-8","wallet":"8RwBhp2Q86SeSWqt8Y2vspR5LfqWmQCdu2wpUTM3cSXS"},
    {"username":"sunny-9","wallet":"4q58evjqN3G6ura5t5rqptLPdDVjCFENFTpeGyR5uPnH"},
    {"username":"sunny-10","wallet":"B1KVMqniFQ9dJJKxq9wvMXWW91zz8R5Q18TANJfbBVRq"},
]

async def handle_modal(page):
    modal = page.locator("#scamMigrationWarningModal")
    try:
        if await modal.is_visible(timeout=5000):
            print("⚠️ Closing modal...")
            buttons = modal.locator("button")
            if await buttons.count() > 0:
                await buttons.first.click()
                await page.wait_for_timeout(1000)
    except:
        pass

async def run_bot():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )

        for acc in accounts:
            context = await browser.new_context()
            page = await context.new_page()

            print("Running account:", acc["username"])

            try:
                await page.goto("https://theros.io/prelaunch", timeout=80000)
                await page.wait_for_load_state("networkidle", timeout=15000)
            except TimeoutError:
                print(f"Timeout for {acc['username']}. Skipping.")
                await context.close()
                continue

            await handle_modal(page)
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_selector("input", timeout=15000)

            inputs = await page.query_selector_all("input")
            if len(inputs) < 2:
                print(f"Not enough inputs for {acc['username']}, skipping")
                await context.close()
                continue

            await inputs[0].fill(acc["username"])
            await inputs[1].fill(acc["wallet"])

            if len(inputs) > 2:
                await inputs[2].fill("bot")

            await handle_modal(page)

            create_btn = page.locator("#registerBtn")
            try:
                await create_btn.click(timeout=9000)
            except TimeoutError:
                await create_btn.click(force=True)

            next_btn = page.locator("#nextQuestionBtn")
            try:
                await next_btn.wait_for(state="visible", timeout=8000)
                await next_btn.click()
            except:
                pass

            answer_selector = f"#answer{ANSWER.upper()}"
            try:
                await page.locator(answer_selector).click(timeout=20000)
                print("Answered:", ANSWER)
            except Exception as e:
                print(f"Failed to answer: {e}")

            await page.wait_for_timeout(1000)
            await context.close()

        await browser.close()
        print("🎉 All accounts processed successfully!")

if __name__ == "__main__":
    asyncio.run(run_bot())
