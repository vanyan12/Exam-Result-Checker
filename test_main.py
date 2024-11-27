import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import time
import datetime
import telebot
import os
import logging
import pytz


logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:',
    filename="Error.log",
    filemode='a'
)

def report_err(e):
    bot.send_message(931534758, e)
    logging.error("Error has occured: %s" ,  str(e))


# ==================================================================

def load(filename="./data.txt"):
    with open(filename, 'r', encoding="utf-8") as file:
        return file.read()
    
def save(data):
    with open('./data.txt', 'w', encoding="utf-8") as file:
        text = ''
        for name in data:
            if name != data[-1]:
                text += f"'{name}',\n"
            else:
                text += f"'{name}'\n"
        file.write(f"[\n{text}\n]")


New = None

Error_time_1 = None
Error_time_2 = None
# ===============================================================

# Default directory to download files
def_dir = rf'C:\Users\Aren\Desktop\CheckerBot\Files' 

TOKEN = '6453916057:AAGzKgo5Ad160ccrZriyo50YKThStYYhkaU'
bot = telebot.TeleBot(TOKEN)

arm_tz = pytz.timezone("Asia/Yerevan")
timeObj = datetime.datetime.now(datetime.timezone.utc)

# ==================================================================

def is_worktime(): # For preventing from runing function in the night and at the weekend

    time = timeObj.astimezone(arm_tz).time()
    day = timeObj.astimezone(arm_tz).weekday()

    return True if time >= datetime.datetime.strptime('09:00:00', '%H:%M:%S').time() and \
                   time <= datetime.datetime.strptime('18:00:00', '%H:%M:%S').time() and \
                   day <= 4 else False

async def send_files(chat_id):
    files = os.listdir(def_dir)

    # Sending all the new files to chat
    for file in files:
        file_path = os.path.join(def_dir, file)

        try:
            with open(file_path, 'rb') as f:
                bot.send_document(chat_id, f)
        except Exception as e:
            logging.error("Error has occured: %s" ,  str(e))




async def delate_files():
    files = os.listdir(def_dir)

    # Delating files from directory
    for file in files:
        file_path = os.path.join(def_dir, file)
        os.remove(file_path)

def handle_error(e):
    global Error_time_1
    global Error_time_2

    if Error_time_1:
        Error_time_2 = timeObj.astimezone(arm_tz)
    else: 
        Error_time_1 = timeObj.astimezone(arm_tz)

    logging.error("Error has occured: %s" ,  str(e))
    bot.send_message("<YOUR-TELEGRAM-ID>", e) # For notifing you about errors

    if Error_time_2 and (Error_time_2 - Error_time_1) >= datetime.timedelta(minutes=3) and (Error_time_2 - Error_time_1) <= datetime.timedelta(minutes=4):
        return
    



# =========================================================================================
async def check(): # For checking whether new files are uploaded

    if is_worktime():

        print("Working...")

        try:
            # DATABASE for comparing with the website data and NEW for saving new data
            Database = load()

            async with async_playwright() as playwright:
                browser = await playwright.chromium.launch(headless=True)
                context = await browser.new_context(accept_downloads=True)
                page = await context.new_page()
                page.set_default_timeout(60000)

                # Login =============================================================
                await page.goto("https://moodle.ufar.am", timeout=60000)

                login_btn = page.locator("//*[@id='main-header']/div/div/div/div[3]/div/div[1]/a")
                await login_btn.click()

                username = page.locator("#login-username")
                await username.fill("<YOUR-USERNAME>")

                password = page.locator("#login-password")
                await password.fill("<PASSWORD>")

                sumbit_btn = page.locator("#header-form-login > button")
                await sumbit_btn.click()

                # Navigation and Scraping =========================================================

                menu = page.locator("//*[@id='site-menu']/div/div/div/ul/li[1]/a")
                await menu.click()

                fac_ima = page.locator("//*[@id='label_3_13']")
                await fac_ima.click()

                year = page.locator("//*[@id='module-21059']/div/div/div[2]/div/a")
                await year.click()
                
                # Choosing IMA2
                ima2 = await page.wait_for_selector("//*[@id='ygtvt16']/a", state="visible")
                await ima2.click()

                semester = page.locator("//*[@id='ygtvt17']/a")
                await semester.click()

                table_div_inner_html =  await page.locator("//*[@id='ygtvc17']").inner_html()

                html = BeautifulSoup(table_div_inner_html, "html.parser")

                span_tags = html.find_all('span', class_= "fp-filename")

                file_names = [span.text for span in span_tags]

                print(file_names)
                print(Database)


                # Checking whether there are some files that are not in the Database, and if there are downloading them
                if len(file_names) != len(Database):
                    New = [name for name in file_names if name not in Database]


                    # Downloading files ============================
                    for name in New:

                        async with page.expect_download() as download_handler:
                            span = page.locator(f"//span[@class='fp-filename' and text()='{name}']")
                            await span.click()

                            download = await download_handler.value       

                            file_path = f"{def_dir}/{download.suggested_filename}"

                            await download.save_as(file_path)


                    # Sending files and delating ================== 

                    chat_id = "<YOUR-CHAT-ID>" # IM2 chat
                    await send_files(chat_id)
                    await delate_files()

                    # Updating Database ========================================
                    # Database = file_names[:]
                    save(file_names[:])


        except Exception as e:
            handle_error(e)
        
        finally:
            await browser.close()
            
    else:
        print("Is not working hour")

async def main():
    while True:
        await check()
        await asyncio.sleep(180) # Frequency of checkings with seconds

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program interrupted.")


