import sys, asyncio, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Usage : python3 _gabarit/shoot.py <dossier>  -> captures ordinateur + mobile dans _gabarit/shots/
from playwright.async_api import async_playwright
async def main(name):
    os.makedirs(os.path.join(ROOT, '_gabarit', 'shots'), exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--no-sandbox'])
        for w,h,tag in ((1280,800,'d'),(390,800,'m')):
            pg = await b.new_page(viewport={'width':w,'height':h})
            errs=[]
            pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.goto('file://' + os.path.join(ROOT, name, 'index.html'))
            await pg.wait_for_timeout(600)
            await pg.screenshot(path=os.path.join(ROOT, '_gabarit', 'shots', f'{name}-{tag}-top.png'))
            await pg.screenshot(path=os.path.join(ROOT, '_gabarit', 'shots', f'{name}-{tag}-full.png'), full_page=True)
            sw = await pg.evaluate('document.documentElement.scrollWidth')
            print(name, tag, 'scrollWidth', sw, 'errors', errs)
        await b.close()
asyncio.run(main(sys.argv[1]))
