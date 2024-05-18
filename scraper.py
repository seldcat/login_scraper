import asyncio
from playwright.async_api import async_playwright


async def scroll_to_bottom(page):
    previous_height = None
    while True:
        current_height = await page.evaluate('document.body.scrollHeight')
        if current_height == previous_height:
            break
        previous_height = current_height
        await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        await page.wait_for_timeout(2000)  # Ждем 2 секунды


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # headless=True для безголового режима
        context = await browser.new_context()
        page = await context.new_page()

        # start_urls = [
        #     'https://www.reddit.com/r/todayilearned/',
        #     'https://www.reddit.com/r/news/',
        #     'https://www.reddit.com/r/interestingasfuck/',
        #     'https://www.reddit.com/r/funny/',
        #     'https://www.reddit.com/r/AskReddit/'
        # ]

        # Переходим на целевую страницу
        await page.goto('https://www.reddit.com/r/news/')

        # Определяем селекторы
        post_selector = 'a[slot=full-post-link]'
        comment_login_selector = 'a[href^="/user/"]'

        # Прокручиваем страницу до самого низа для загрузки всех постов
        await scroll_to_bottom(page)

        # Получаем все посты
        posts = await page.query_selector_all(post_selector)
        print(f'Найдено постов: {len(posts)}')

        # Проходим по каждому посту
        for post in posts:
            # Кликаем на пост
            try:
                await post.click()
            except Exception:
                continue

            # Ждем загрузки страницы поста
            await page.wait_for_selector('#main-content > shreddit-async-loader > comment-body-header > faceplate-tracker')

            # Прокручиваем страницу поста до самого низа для загрузки всех комментариев
            await scroll_to_bottom(page)

            # Получаем все логины из комментариев
            comment_logins = await page.query_selector_all(comment_login_selector)
            logins = [await login.text_content() for login in comment_logins]
            logins = list(set(map(lambda x: x.strip(), logins)))
            print(f'Логины из комментариев: {", ".join(logins)}')

            # Возвращаемся на главную страницу
            await page.go_back()

            # Ждем, пока снова загрузятся все посты (если необходимо)
            await page.wait_for_selector(post_selector)

        # Закрываем браузер
        await browser.close()


# Запуск асинхронного основного процесса
asyncio.run(main())
