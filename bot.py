import asyncio
from playwright.async_api import async_playwright, TimeoutError

ANSWER = "B"

accounts = [
{"username": "MAS-76", "wallet": "DCRFK1GPNENNWhWBmJZjX5XfnduoDmrhL9aCPnBXoFyR"},
{"username": "MAS-77", "wallet": "GgHgrn3VeWvx9NBZKjcVqqZuMHVkzogHiNMoqkPfoUQk"},
{"username": "MAS-78", "wallet": "CrJUcfM3wAtKFyxuaXzuTAp5try3QWcRjb2sMrtmMmey"},
{"username": "MAS-79", "wallet": "65JnrxHDWcX18XE2PtrG4ag18wGJV7c3tKpDEiU9Q54f"},
{"username": "MAS-80", "wallet": "4gRr3xRcPSzLrUcxHtwe7g5CDnNoUbeBguDHtfZxPeAP"},
{"username": "MAS-81", "wallet": "CoWZJ7c76ythGQvLTLjgi4do45WUxjFXEvVcmABV97M7"},
{"username": "MAS-82", "wallet": "6h7PvCohwXvnNNRiQ5A8PYHMcgpNTJvdvDZQsKkcyNyK"},
{"username": "MAS-83", "wallet": "5BquBP7Lk8NMpyz5H65vBctCJsbLYYaUxJzjScE1p6HT"},
{"username": "MAS-84", "wallet": "Cvza2YZT1xgMjaRKFYe3LpALKgKqMaco7MjBcvu58MUk"},
{"username": "MAS-85", "wallet": "huDFyJrsXVJUN9ocHd4rxT6UfW9sGMJCoCQGj3o1Jct"},
{"username": "MAS-86", "wallet": "B2CPH5JawS6dJqjw3J13YNKhD2McqRn8JWHvNMr5aLLD"},
{"username": "MAS-87", "wallet": "5ovAsUUKVvNenewZg9jsZSkx3JPabWJPYSqrNfSBdwZY"},
{"username": "MAS-88", "wallet": "9iw7AhmrS6q8BXzWa6us5SeaTSino7gAcSGgdrCPqgWJ"},
{"username": "MAS-89", "wallet": "CzR7TFS1qdm1W9bUAqiv5vWgquwapyFYT7NuoxtwbsLs"},
{"username": "MAS-90", "wallet": "23M9iPMVUsWN2P4X8YMGKVn19EnfexPwWzWyGDDaBYt5"},
{"username": "MAS-91", "wallet": "634VazfFyiRbdPSoeq1sAZSnrBMgzN9UhFAUq3grjxh6"},
{"username": "MAS-92", "wallet": "4pRjFGbqF6uUZ9xcLFu2X3twWPKxiiPqWyMC1zXmgUhc"},
{"username": "MAS-93", "wallet": "AEQugbkyMyXzHyCrNWt29SaHVxkPDvBZUk6BTiTVNvRp"},
{"username": "MAS-94", "wallet": "3q1caMHJhahRUM6nGGv2nxjV4PmpoBCRfCNuZJnGybSu"},
{"username": "MAS-95", "wallet": "HBMydXDaJFD2TeUe9yK5Z7Uq4hqgeH5VF7Y8shVqHEbj"},
{"username": "MAS-96", "wallet": "7VrEE9im4wR6uvAeCMnd5H3umFXpS5Dn1xai5Y9UU3tW"},
{"username": "MAS-97", "wallet": "Bm7JePPSkHxph9nCA8LgFLfvixwEjB3LGkG556b9iXFr"},
{"username": "MAS-98", "wallet": "FgtL2nTJC3p6sAHXzRdk9HutjJ98mcEmTFomJTq4dBxR"},
{"username": "MAS-99", "wallet": "AJGgjmzgihDgwWZ4e82weijy7mM3K3sDRojbJrASAtA5"},
{"username": "MAS-100", "wallet": "8ffKJnRjpTKx4RaniuQNdJ1wBN1A4MKusHrApCYXDhvi"},
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
