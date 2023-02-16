from tkinter import *
from tkinter import ttk, messagebox
#from tkextrafont import Font
import time
import os
import sqlite3
import store_db as sdb
from store_db import add_game, get_games, del_game, get_library_games, add_library_game, get_library_games_all_data
import add_money
import matplotlib.pyplot as mlt
import numpy as nmpi

addMoneyCanvasLabel = None

selected_game_ids = []
appCount = 0

def main_app():
    GAMES = [
    {
        "id": 0,
        "name": "Stardew Valley",
        "publisher": "ConcernedApe",
        "tag": "Game / Entertainment",
        "price": 419.95,
        "image": "./asset/app_images/libraryitem1.png",
    },
    {
        "id": 1,
        "name": "Wallpaper Engine",
        "publisher": "Wallpaper Engine Team",
        "tag": "Software Utility",
        "price": 135.95,
        "image": "./asset/app_images/libraryitem2.png",
    },
    {
        "id": 2,
        "name": "Kingdom Rush: Origins",
        "publisher": "",
        "tag": "",
        "price": 2300.0,
        "image": "./asset/app_images/libraryitem3.png",
    },
    {
        "id": 3,
        "name": "Plaque Inc.",
        "publisher": "",
        "tag": "",
        "price": 301.46,
        "image": "./asset/app_images/libraryitem4.png",
    }
]
    #Go to library page
    def displayLibrary(event):
        storeFrame.pack_forget()
        storeCanvasLabel.itemconfig(store_label, font="Inter 28", fill="#969696")
        cartFrame.pack_forget()
        cartCanvasLabel.itemconfig(cart_label, image=cart_gray)
        libraryCanvas.pack(side="left", fill=BOTH, expand=True)
        libraryCanvasLabel.itemconfig(lib_label, font="Inter 28 underline", fill="#FFFFFF")

    #Go to store page
    def displayStore(event):
        libraryCanvas.pack_forget()
        libraryCanvasLabel.itemconfig(lib_label, font="Inter 28", fill="#969696")
        cartFrame.pack_forget()
        cartCanvasLabel.itemconfig(cart_label, image=cart_gray)
        storeFrame.pack(fill=BOTH, expand=True)
        storeCanvasLabel.itemconfig(store_label, font="Inter 28 underline", fill="#FFFFFF")
        
    #Go to cart page
    def displayCart(event):
        libraryCanvas.pack_forget()
        libraryCanvasLabel.itemconfig(lib_label, font="Inter 28", fill="#969696")
        storeFrame.pack_forget()
        storeCanvasLabel.itemconfig(store_label, font="Inter 28", fill="#969696")
        cartFrame.pack(fill=BOTH, expand=True)
        cartCanvasLabel.itemconfig(cart_label, image=cart_white)

    #Logging out
    def openAccount(event):
        def go_to_login():
            mainWindow.destroy()
            main_account_screen()
            
        def cancel_clicked():
            accountWindow.destroy()
        
        accountWindow = Toplevel()
        accountWindow.geometry("500x200")
        accountWindow.title("Account Management")
        accountWindow.config(background="#192334")
        accountWindow.grab_set()
        
        questionLabel = Label(accountWindow, text="Logout Account?", font=('Inter', 18), fg="white", bg="#192334")
        questionLabel.pack(pady=(40, 30))
        
        buttonFrame = Frame(accountWindow, bg="#192334")
        buttonFrame.pack()
        
        logoutButton = Button(buttonFrame, text="Logout", font=('Inter', 14), fg="#101723", bg="white", bd=0, width=10, cursor="hand2", command=go_to_login)
        logoutButton.grid(row=0, column=0, padx=20)
        
        cancelButton = Button(buttonFrame, text="Cancel", font=('Inter', 14), fg="white", bg="#101723", bd=0, width=10, cursor="hand2", command=cancel_clicked)
        cancelButton.grid(row=0, column=1)

    #Open add money window
    def addMoney(event):
        #Restricts input to entrybox, allows only proper int/float value format
        def callback(P):
            if str.isdigit(P) or ("." in P):
                period = 0 
                for i in P:
                    if i.isalpha():
                        return False
                    elif i == ".":
                        period=period+1
                if period > 1:
                    return False
                return True
            elif P == "":
                return True
            else:
                return False
        
        #Placeholder function for selected radiobutton
        def get_cardtype():
            if chosen.get()==0:
                print("Visa")
            elif chosen.get()==1:
                print("Mastercard")
            elif chosen.get()==2:
                print("Gcash")
            else:
                print("huh?")
                
        def confirm_clicked():
            # add balance 
            if (len(cashAmountEntry.get().strip()) == 0):
                messagebox.showwarning('Invalid Amount', 'Enter amount value')
            elif (len(cashPinEntry.get().strip()) == 0):
                messagebox.showwarning('Invalid PIN', 'Enter PIN value')
            else:
                add_money.add_credits(add_money.get_misc_user(), cashAmountEntry.get(), cashPinEntry.get())
                # update balance text
                addMoneyCanvasLabel.delete("balance_tag")
                addMoneyCanvasLabel.create_text((60, 20), text=f"₱ {add_money.get_balance(add_money.get_misc_user())}", font=('Inter', 12), fill="white", tag="balance_tag")   
                addMoneyWindow.destroy()
                update_summary()
                          
            


        def cancel_clicked():
            addMoneyWindow.destroy()
            
        addMoneyWindow = Toplevel()
        addMoneyWindow.geometry("300x340")
        addMoneyWindow.title("Add Funds")
        addMoneyWindow.config(background="#192334")
        addMoneyWindow.resizable(False,False)
        addMoneyWindow.grab_set()
        
        #global chosen
        
        cashHeaderFrame = Frame(addMoneyWindow, bg="#101723", height=75)
        cashHeaderFrame.pack(fill=X)
        
        cashHeaderLabel = Label(cashHeaderFrame, text="Add Money", fg="white", bg="#101723", font=('Inter', 20))
        cashHeaderLabel.pack(fill="both", pady=(30,10))
        
        cashBodyFrame = Frame(addMoneyWindow, bg="#192334")
        cashBodyFrame.pack(fill="both")
        
        #Cash Amount Section
        cashAmountFrame = Frame(cashBodyFrame, bg="#192334")
        cashAmountFrame.pack(pady=(20,0))
        
        cashAmountLabel = Label(cashAmountFrame, text="Amount", fg="white", bg="#192334", font=('Inter', 13))
        cashAmountLabel.pack(anchor=W, pady=(0,2))
        
        vcmd = (cashAmountFrame.register(callback))
        cashAmountEntry = Entry(cashAmountFrame, font=('Inter', 15), fg="black", bg='white', validate='key', validatecommand=(vcmd, '%P'), width=18)
        cashAmountEntry.pack()
        
        #Groups card type and card pin frames
        cashDetailFrame = Frame(cashBodyFrame, bg="#192334")
        cashDetailFrame.pack(fill='both', pady=(20,0))
        
        #Card Type Section
        cashOptionFrame = Frame(cashDetailFrame, bg="#192334")
        cashOptionFrame.pack(side=LEFT, fill='both', expand=True, padx=(28,20))
        
        optionRadioButton1 = Radiobutton(cashOptionFrame, text="Visa", variable=chosen, value=0, font=('Inter', 10), fg="white", bg="#192334", 
                                        selectcolor="black", command=get_cardtype, indicatoron=1, width=10, anchor=W, padx=0,
                                        activeforeground="white", activebackground="#192334", cursor="hand2")
        optionRadioButton1.pack(anchor=W)
                
        optionRadioButton2 = Radiobutton(cashOptionFrame, text="Mastercard", variable=chosen, value=1, font=('Inter', 10), fg="white", bg="#192334", 
                                        selectcolor="black", command=get_cardtype, indicatoron=1, width=10, anchor=W, padx=0,
                                        activeforeground="white", activebackground="#192334", cursor="hand2")
        optionRadioButton2.pack(anchor=W)
                
        optionRadioButton3 = Radiobutton(cashOptionFrame, text="Gcash", variable=chosen, value=2, font=('Inter', 10), fg="white", bg="#192334", 
                                        selectcolor="black", command=get_cardtype, indicatoron=1, width=10, anchor=W, padx=0,
                                        activeforeground="white", activebackground="#192334", cursor="hand2")
        optionRadioButton3.pack(anchor=W)
        
        #Cash Pin Section
        cashSecurityFrame = Frame(cashDetailFrame, bg="#192334")
        cashSecurityFrame.pack(side=RIGHT, fill='both', expand=True)
        
        cashPinLabel = Label(cashSecurityFrame, text="Enter PIN", font=('Inter', 10), fg="white", bg="#192334")
        cashPinLabel.pack(anchor=SW, padx=(13,0), pady=(25,0))
        
        cashPinEntry = Entry(cashSecurityFrame, show="*", font=('Inter', 13), fg="black", bg="white", width=7)
        cashPinEntry.pack(anchor=SE, padx=(0,32))
        
        #Cash Confirm / Cancel Buttons
        cashButtonFrame = Frame(cashBodyFrame, bg="#192334")
        cashButtonFrame.pack(pady=(30,0))
        
        cashConfirmButton = Button(cashButtonFrame, text="Confirm", font=('Inter', 12), fg="white", bg="#232F3E", bd=0, width=9, cursor="hand2", command=confirm_clicked)
        cashConfirmButton.grid(row=0, column=0, padx=(0,20))
        
        cashCancelButton = Button(cashButtonFrame, text="Cancel", font=('Inter', 12), fg="white", bg="#232F3E", bd=0, width=9, cursor="hand2", command=cancel_clicked)
        cashCancelButton.grid(row=0, column=1)

    def get_users_cart_games(username):
        game_ids_in_cart = get_games(username)

        result = []

        for game_id in game_ids_in_cart:
            games = [game for game in GAMES if game["id"] == game_id]

            if len(games) > 0:
                result.append(games[0])

        return result
    
    def get_users_library_games(username):
        game_ids_in_cart = get_library_games(username)

        result = []

        for game_id in game_ids_in_cart:
            games = [game for game in GAMES if game["id"] == game_id]

            if len(games) > 0:
                result.append(games[0])

        return result
    
    def is_game_already_owned(game_id):
        games = get_users_library_games(add_money.get_misc_user())

        for game in games:
            if game["id"] == game_id:
                return True

        return False

    def example_add_function(game_id):
        pop_up_screen = Toplevel(mainWindow)
        pop_up_screen.title("")
        pop_up_screen.geometry('200x100+550+300')
        pop_up_screen.configure(bg="#192334")
        pop_up_screen.resizable(False, False)

        is_owned = is_game_already_owned(game_id)

        message = "Added to Cart Succesfully!"

        if is_owned:
            message = "Already in your library"
        else:
            try:
                add_game(game_id, add_money.get_misc_user())
            except Exception as e:
                message = "Already in your cart"
                print(e)

        update_item_list()
        Label(pop_up_screen, text=message, font=('Inter 10'), fg='#ffffff', bg="#192334").place(x=30, y=15)
        Button(pop_up_screen, width=9, pady=1, text='OK', bg='#101723', font=('Inter 10'), fg='#ffffff',
                            border=0, cursor="hand2", command=lambda: pop_up_screen.destroy()).place(x=60, y=50)
        
    def showGraph(event):

        games_in_library = get_library_games_all_data(add_money.get_misc_user())

        result = []


        for game in games_in_library:
            games = [x for x in GAMES if x["id"] == game[1]]

            if len(games) > 0:
                result.append(game)

        graphMonths = nmpi.array([game[3][:-7] for game in result])
        graphValues = nmpi.array([game[2] for game in result])

        mlt.title("Your purchase value")
        # mlt.xlabel("Months")
        mlt.ylabel("Total Expenses")

        mlt.bar(graphMonths, graphValues)
        mlt.show()

    #When trash clicked
    def removeItem(event):
        for game_id in selected_game_ids:
            del_game(game_id, add_money.get_misc_user())

        update_item_list()
        print("Item Removed")
        
    def buyCart():
        def progressBar():
            tasks = 200
            x = 0
            while(x<tasks):
                time.sleep(0.025)
                bar['value']+=0.5
                if x < 66:
                    detail.set("Verifying Payment Details")
                elif x >= 66 and x < 150:
                    detail.set("Processing Purchase Logistics")
                else:
                    detail.set("Completing Transaction")
                x+=1
                progressWindow.update()
            progressWindow.destroy()

            for game in get_users_cart_games(add_money.get_misc_user()):
                add_library_game(game["id"], add_money.get_misc_user(), game["price"])
                del_game(game["id"], add_money.get_misc_user())
                add_money.remove_credits(add_money.get_misc_user(), game["price"], "")
                

            update_library()
            update_item_list()
            update_games_in_store()
            update_account_frame()
            
        def on_closing():
            pass
            
        progressWindow = Toplevel()
        progressWindow.resizable(False,False)
        detail = StringVar()
        bar = ttk.Progressbar(progressWindow, orient=HORIZONTAL, length=300)
        bar.pack(pady=10,padx=10)
        processDetailLabel = Label(progressWindow, textvariable=detail)
        processDetailLabel.pack()
        
        #Does not allow the process to be canceled
        progressWindow.protocol("WM_DELETE_WINDOW", on_closing)
        
        progressBar()
        
        print("Bought Cart")

    #Create Main Window
    mainWindow = Tk()
    mainWindow.geometry("1280x700")
    mainWindow.title("EaseBuy App Store")
    mainWindow.config(background="#101723")
    mainWindow.resizable(False,False)

    chosen = IntVar() #variable for radiobuttons in add money window

    #Font(file="./asset/Inter-Regular.ttf", family="Inter")

    #Declare Images-------------------------------------------------------------------------------------------
    #Declare Images-------------------------------------------------------------------------------------------
    cart_white = PhotoImage(file="./asset/bx-cart-white.png")
    cart_gray = PhotoImage(file="./asset/bx-cart-gray.png")
    graph_icon = PhotoImage(file="./asset/bx-graph.png")

    libraryItemPhoto1 = PhotoImage(file="./asset/app_images/libraryitem1.png")
    libraryItemPhoto2 = PhotoImage(file="./asset/app_images/libraryitem2.png")
    libraryItemPhoto3 = PhotoImage(file="./asset/app_images/libraryitem3.png")
    libraryItemPhoto4 = PhotoImage(file="./asset/app_images/libraryitem4.png")

    for game in GAMES:
        if type (game["image"]) == str:
            game["image"] = PhotoImage(file=game["image"])

    appFrameBg = PhotoImage(file="./asset/applibrarybg.png")
    librarybg = PhotoImage(file="./asset/librarybg.png")
    addmoneybg = PhotoImage(file="./asset/addmoneybg.png")
    cartbg = PhotoImage(file="./asset/cartbodybg.png")
    trash_icon = PhotoImage(file="./asset/bx-trash.png")
    store_framebg = PhotoImage(file="./asset/Storeframebg .png")
    appstore_framebg = PhotoImage(file="./asset/appframestorebg.png")


    #Display scrollbar when needed
    def checkScrollbar(event):
        #global appCount
        if appCount>=4:
            scrollbar.pack(side="right", fill="y")

    #Window Frame
    mainFrame = Frame(mainWindow, bg="#101723")
    mainFrame.pack(expand=True, fill="both")

    #Tab Frame
    tabFrame = Frame(mainFrame, bg="#101723")
    tabFrame.pack(fill=X, pady=(15,0))

    #Body Frame
    bodyFrame = Frame(mainFrame, bg="#101723")
    bodyFrame.pack(fill=BOTH, expand=True, padx=30, pady=(0,20))

    #Library Tab Button
    libraryCanvasLabel = Canvas(tabFrame, width=150, height=50, bg="#101723", highlightthickness=0, cursor="hand2")
    libraryCanvasLabel.grid(row=0, column=0, padx=20, pady=20)
    lib_label = libraryCanvasLabel.create_text((80, 20), text="Library", font="Inter 28 underline", fill="#FFFFFF")
    libraryCanvasLabel.bind('<Button-1>', displayLibrary)

    #Store Tab Button
    storeCanvasLabel = Canvas(tabFrame, width=100, height=50, bg="#101723", highlightthickness=0, cursor="hand2")
    storeCanvasLabel.grid(row=0, column=1, padx=20, pady=20)
    store_label = storeCanvasLabel.create_text((50, 20), text="Store", font=('Inter', 28), fill="#969696")
    storeCanvasLabel.bind('<Button-1>', displayStore)

    #Cart Tab Button
    cartCanvasLabel = Canvas(tabFrame, width=50, height=50, bg="#101723", highlightthickness=0, cursor="hand2")
    cartCanvasLabel.grid(row=0, column=2, padx=(0, 700), pady=20)
    cart_label = cartCanvasLabel.create_image((20,20), image=cart_gray)
    cartCanvasLabel.bind('<Button-1>', displayCart)

    #Account / Add Money Section
    accountFrame = Frame(tabFrame, bg="#101723")
    accountFrame.grid(row=0, column=3, padx=20, pady=0, sticky=NE, columnspan=2)

    def update_account_frame():
        global addMoneyCanvasLabel
        for child in accountFrame.winfo_children():
            child.destroy()

        accountCanvasLabel = Canvas(accountFrame, width=120, height=35, bg="#101723", highlightthickness=0, cursor="hand2")
        accountCanvasLabel.pack(side=TOP)
        account_label = accountCanvasLabel.create_text((60, 20), text="Account", font=('Inter', 20), fill="white")
        accountCanvasLabel.bind('<Button-1>', openAccount)

        addMoneyCanvasLabel = Canvas(accountFrame, width=120, height=35, bg="#101723", highlightthickness=0, cursor="hand2")
        addMoneyCanvasLabel.pack(side=TOP)
        addMoneyCanvasLabel.create_image((60,20), image=addmoneybg)
        addMoneyCanvasLabel.create_text((60, 20), text=f"₱ {round(add_money.get_balance(add_money.get_misc_user()), 2)}", font=('Inter', 12), fill="white", tag="balance_tag")
        addMoneyCanvasLabel.bind('<Button-1>', addMoney)

    update_account_frame()


    #Library Body-----------------------------------------------
    def FrameWidth(event):
        canvas_width = libraryCanvas.winfo_width()
        libraryCanvas.itemconfig(canvas_frame, width=canvas_width)
        
    libraryCanvas = Canvas(bodyFrame, highlightthickness=0, bg="#101723")
    scrollbar = Scrollbar(bodyFrame, orient="vertical", command=libraryCanvas.yview, bg="#101723")

    libraryFrame = Frame(libraryCanvas, bg="#101723" )

    libraryFrame.bind("<Configure>",lambda e: libraryCanvas.configure(scrollregion=libraryCanvas.bbox("all")))
    libraryCanvas.bind("<Configure>",FrameWidth)

    canvas_frame = libraryCanvas.create_window((0, 0), window=libraryFrame, anchor="nw")
    libraryCanvas.configure(yscrollcommand=scrollbar.set)

    libraryCanvas.pack(side="left", fill="both", expand=True)
    
    def update_library():
        global appCount
        
        for child in libraryFrame.winfo_children():
            child.destroy()
        
        #Library Background
        libraryBGLabel = Label(libraryFrame, image=librarybg, bd=0, bg="#101723")
        libraryBGLabel.place(x=0, y=0)
        libraryBGLabel.bind("<Configure>", checkScrollbar)

        for game in get_users_library_games(add_money.get_misc_user()):
            #-----Library App Owned Sample 1-----
            appLibraryFrame1 = Frame(libraryFrame, height=120, bg="#101723")
            appLibraryFrame1.pack(fill=X, padx=20, pady=20)

            #Blue-ish background of each individual app
            appBGLabel = Label(appLibraryFrame1, image=appFrameBg, bd=0, bg="#192334")
            appBGLabel.place(x=0, y=0)

            #Groups App photo, App name, and Developer Name to be displayed on the left section
            appLeftSectionFrame1 = Frame(appLibraryFrame1, bg="#232F3E")
            appLeftSectionFrame1.pack(side=LEFT)

            appPhotoFrame = Frame(appLeftSectionFrame1, bg="#232F3E")
            appPhotoFrame.pack(side=LEFT)
            appPhotoLabel1 = Label(appPhotoFrame, image=game["image"], bg="#232F3E", width=120, height=120, bd=0)
            appPhotoLabel1.pack()

            #Groups App name and Developer name displayed top to bottom
            appInfoFrame = Frame(appLeftSectionFrame1, bg="#232F3E")
            appInfoFrame.pack(side=LEFT)

            #Labels for App Name, Developer Name, App Type
            appNameLabel1 = Label(appInfoFrame, text=game["name"], bg="#232F3E", font=('Inter', 22, 'bold'), fg="white")
            appNameLabel1.grid(row=0, column=1, padx=10, sticky=W)
            appDevLabel1 = Label(appInfoFrame, text=game["publisher"], bg="#232F3E", font=('Inter', 14), fg="white")
            appDevLabel1.grid(row=1, column=1, padx=12, sticky=W)
            appTypeLabel1 = Label(appLibraryFrame1, text=game["tag"], bg="#232F3E", font=('Inter', 14), fg="white")
            appTypeLabel1.pack(side=RIGHT, padx=20)
            appCount += 1

    update_library()
    # #-----Library App Owned Sample 1-----
    # appLibraryFrame1 = Frame(libraryFrame, height=120, bg="#101723")
    # appLibraryFrame1.pack(fill=X, padx=20, pady=20)

    # #Blue-ish background of each individual app
    # appBGLabel = Label(appLibraryFrame1, image=appFrameBg, bd=0, bg="#192334")
    # appBGLabel.place(x=0, y=0)

    # #Groups App photo, App name, and Developer Name to be displayed on the left section
    # appLeftSectionFrame1 = Frame(appLibraryFrame1, bg="#232F3E")
    # appLeftSectionFrame1.pack(side=LEFT)

    # appPhotoFrame = Frame(appLeftSectionFrame1, bg="#232F3E")
    # appPhotoFrame.pack(side=LEFT)
    # appPhotoLabel1 = Label(appPhotoFrame, image=libraryItemPhoto1, bg="#232F3E", width=120, height=120, bd=0)
    # appPhotoLabel1.pack()

    # #Groups App name and Developer name displayed top to bottom
    # appInfoFrame = Frame(appLeftSectionFrame1, bg="#232F3E")
    # appInfoFrame.pack(side=LEFT)

    # #Labels for App Name, Developer Name, App Type
    # appNameLabel1 = Label(appInfoFrame, text="Stardew Valley", bg="#232F3E", font=('Inter', 22, 'bold'), fg="white")
    # appNameLabel1.grid(row=0, column=1, padx=10, sticky=W)
    # appDevLabel1 = Label(appInfoFrame, text="ConcernedApe", bg="#232F3E", font=('Inter', 14), fg="white")
    # appDevLabel1.grid(row=1, column=1, padx=12, sticky=W)
    # appTypeLabel1 = Label(appLibraryFrame1, text="Game / Entertainment", bg="#232F3E", font=('Inter', 14), fg="white")
    # appTypeLabel1.pack(side=RIGHT, padx=20)

    # #-----Library App Owned Sample 2-----
    # appLibraryFrame1 = Frame(libraryFrame, height=120, bg="#101723")
    # appLibraryFrame1.pack(fill=X, padx=20, pady=20)

    # #Blue-ish background of each individual app
    # appBGLabel = Label(appLibraryFrame1, image=appFrameBg, bd=0, bg="#192334")
    # appBGLabel.place(x=0, y=0)

    # #Groups App photo, App name, and Developer Name to be displayed on the left section
    # appLeftSectionFrame1 = Frame(appLibraryFrame1, bg="#232F3E")
    # appLeftSectionFrame1.pack(side=LEFT)

    # appPhotoFrame = Frame(appLeftSectionFrame1, bg="#232F3E")
    # appPhotoFrame.pack(side=LEFT)
    # appPhotoLabel1 = Label(appPhotoFrame, image=libraryItemPhoto2, bg="#232F3E", width=120, height=120, bd=0)
    # appPhotoLabel1.pack()

    # #Groups App name and Developer name displayed top to bottom
    # appInfoFrame = Frame(appLeftSectionFrame1, bg="#232F3E")
    # appInfoFrame.pack(side=LEFT)

    # #Labels for App Name, Developer Name, App Type
    # appNameLabel1 = Label(appInfoFrame, text="Wallpaper Engine", bg="#232F3E", font=('Inter', 22, 'bold'), fg="white")
    # appNameLabel1.grid(row=0, column=1, padx=10, sticky=W)
    # appDevLabel1 = Label(appInfoFrame, text="Wallpaper Engine Team", bg="#232F3E", font=('Inter', 14), fg="white")
    # appDevLabel1.grid(row=1, column=1, padx=12, sticky=W)
    # appTypeLabel1 = Label(appLibraryFrame1, text="Software Utility", bg="#232F3E", font=('Inter', 14), fg="white")
    # appTypeLabel1.pack(side=RIGHT, padx=20)

    #Store Body -------------------------------------------------------------------------------------------------------

    storeFrame = Frame(bodyFrame, bg="#192334")
    storeBGLabel = Label(storeFrame, image=store_framebg, bd=0, bg="#101723")
    storeBGLabel.place(x=0, y=0)
    storeBGLabel.bind("<Configure>", checkScrollbar)

    #store container
    appstoreFrame1 = Frame(storeFrame, height=400, bg="#192334")
    appstoreFrame1.pack(fill=X, padx=20, pady=20)

    COLUMN_LENGTH = 4

    def create_game_in_store(game, index):
        column = index % COLUMN_LENGTH
        row = index // COLUMN_LENGTH
        appstoreBGLabel1 = Label(appstoreFrame1, image=appstore_framebg, bd=0, bg="#192334")
        appstoreBGLabel1.grid(column=column, row=row, sticky=W, padx=30, pady=10)
        app_storeInfoFrame = Frame(appstoreFrame1, bg="#232F3E")
        app_storeInfoFrame.grid(column=column, row=row, padx=30, pady=10)


        gameImage = Label(app_storeInfoFrame, image=game["image"], bg="#232F3E")
        gameImage.grid(column=0, row=0, sticky=N)
        gamelabel = Label(app_storeInfoFrame, text=game["name"], bg="#232F3E", font=('Inter', 12, 'bold'), fg="white")
        gamelabel.grid(column=0, row=1, sticky=N)
        appDevLabel1 = Label(app_storeInfoFrame, text="ConcernedApe", bg="#232F3E", font=('Inter', 10), fg="white")
        appDevLabel1.grid(column=0, row=2, sticky=S)
        is_owned = is_game_already_owned(game["id"])

        if not is_owned:
            gameButton = Button(app_storeInfoFrame, width=8, pady=1, text=game["price"], bg='#101723', font=('Inter 10'), fg='#ffffff',
                            border=0, cursor="hand2", command=lambda : example_add_function(game["id"]))
            gameButton.grid(column=0, row=3, sticky=S, pady=10)
        else:
            gameButton = Button(app_storeInfoFrame, width=8, pady=1, text="In Library", bg='#101723', font=('Inter 10'), fg='#ffffff',
                            border=0, cursor="hand2", command=lambda : example_add_function(game["id"]))
            gameButton.grid(column=0, row=3, sticky=S, pady=10)

    
    def update_games_in_store():
        for child in appstoreFrame1.winfo_children():
            child.destroy()

        for index, game in enumerate(GAMES):
            create_game_in_store(game, index)

    update_games_in_store()

    # #store frame box1 and grouping- StardewValley
    # appstoreBGLabel1 = Label(appstoreFrame1, image=appstore_framebg, bd=0, bg="#192334")
    # appstoreBGLabel1.grid(column=0, row=0, sticky=W, padx=30, pady=10)
    # app_storeInfoFrame = Frame(appstoreFrame1, bg="#232F3E")
    # app_storeInfoFrame.grid(column=0, row=0, padx=30, pady=10)

    # #App photo, App name, Developer Name and  price button to be displayed inside the frame box using grid -StardewValley

    # appPhotoLabel1 = Label(app_storeInfoFrame, image=libraryItemPhoto1, bg="#232F3E")
    # appPhotoLabel1.grid(column=0, row=0, sticky=N)
    # appNameLabel1 = Label(app_storeInfoFrame, text="Stardew Valley", bg="#232F3E", font=('Inter', 12, 'bold'), fg="white")
    # appNameLabel1.grid(column=0, row=1, sticky=N)
    # appDevLabel1 = Label(app_storeInfoFrame, text="ConcernedApe", bg="#232F3E", font=('Inter', 10), fg="white")
    # appDevLabel1.grid(column=0, row=2, sticky=S)
    # appPriceBtn1 = Button(app_storeInfoFrame, width=8, pady=1, text='419.95', bg='#101723', font=('Inter 10'), fg='#ffffff',
    #                     border=0, cursor="hand2", command=lambda : example_add_function("0"))
    # appPriceBtn1.grid(column=0, row=3, sticky=S, pady=10)

    # #store frame box2 and grouping- Wallpaper Engine
    # appstoreBGLabel1 = Label(appstoreFrame1, image=appstore_framebg, bd=0, bg="#192334")
    # appstoreBGLabel1.grid(column=1, row=0,  padx=30, pady=10)
    # app_storeInfoFrame = Frame(appstoreFrame1, bg="#232F3E")
    # app_storeInfoFrame.grid(column=1, row=0, padx=30, pady=10)

    # #App photo, App name, Developer Name and  price button to be displayed inside the frame box using grid -Wallpaper Engine
    # appPhotoLabel1 = Label(app_storeInfoFrame, image=libraryItemPhoto2, bg="#232F3E")
    # appPhotoLabel1.grid(column=1, row=0, sticky=N)
    # appNameLabel1 = Label(app_storeInfoFrame, text="Wallpaper Engine", bg="#232F3E", font=('Inter', 12, 'bold'), fg="white")
    # appNameLabel1.grid(column=1, row=1, sticky=N)
    # appDevLabel1 = Label(app_storeInfoFrame, text="Wallpaper Engine Team", bg="#232F3E", font=('Inter', 10), fg="white")
    # appDevLabel1.grid(column=1, row=2, sticky=S)
    # appPriceBtn1 = Button(app_storeInfoFrame, width=8, pady=1, text='135.95', bg='#101723', font=('Inter 10'), fg='#ffffff',
    #                     border=0, cursor="hand2", command=lambda : example_add_function("1"))
    # appPriceBtn1.grid(column=1, row=3, sticky=S, pady=10)

    # #store frame box3 and grouping- Kingdom rush
    # appstoreBGLabel1 = Label(appstoreFrame1, image=appstore_framebg, bd=0, bg="#192334")
    # appstoreBGLabel1.grid(column=2, row=0,  padx=30, pady=10)
    # app_storeInfoFrame = Frame(appstoreFrame1, bg="#232F3E")
    # app_storeInfoFrame.grid(column=2, row=0, padx=30, pady=10)

    # #App photo, App name, Developer Name and  price button to be displayed inside the frame box using grid -Kingdom Rush
    # appPhotoLabel1 = Label(app_storeInfoFrame, image=libraryItemPhoto3, bg="#232F3E")
    # appPhotoLabel1.grid(column=2, row=0, sticky=N)
    # appNameLabel1 = Label(app_storeInfoFrame, text="Kingdom Rush: Origins", bg="#232F3E", font=('Inter', 12, 'bold'), fg="white")
    # appNameLabel1.grid(column=2, row=1, sticky=N)
    # appDevLabel1 = Label(app_storeInfoFrame, text="Ironhide Game Studio", bg="#232F3E", font=('Inter', 10), fg="white")
    # appDevLabel1.grid(column=2, row=2, sticky=S)
    # appPriceBtn1 = Button(app_storeInfoFrame, width=8, pady=1, text='2,300.00', bg='#101723', font=('Inter 10'), fg='#ffffff',
    #                     border=0, cursor="hand2", command=lambda : example_add_function("2"))
    # appPriceBtn1.grid(column=2, row=3, sticky=S, pady=10)

    # #store frame box4 and grouping- Plaque Inc.
    # appstoreBGLabel1 = Label(appstoreFrame1, image=appstore_framebg, bd=0, bg="#192334")
    # appstoreBGLabel1.grid(column=3, row=0,  padx=30, pady=10)
    # app_storeInfoFrame = Frame(appstoreFrame1, bg="#232F3E")
    # app_storeInfoFrame.grid(column=3, row=0, padx=30, pady=10)

    # #App photo, App name, Developer Name and  price button to be displayed inside the frame box using grid -Planque Inc
    # appPhotoLabel1 = Label(app_storeInfoFrame, image=libraryItemPhoto4, bg="#232F3E")
    # appPhotoLabel1.grid(column=3, row=0, sticky=N)
    # appNameLabel1 = Label(app_storeInfoFrame, text="Plaque Inc.", bg="#232F3E", font=('Inter', 12, 'bold'), fg="white")
    # appNameLabel1.grid(column=3, row=1, sticky=N)
    # appDevLabel1 = Label(app_storeInfoFrame, text="Ndemic Creations", bg="#232F3E", font=('Inter', 10), fg="white")
    # appDevLabel1.grid(column=3, row=2, sticky=S)
    # appPriceBtn1 = Button(app_storeInfoFrame, width=8, pady=1, text='301.46', bg='#101723', font=('Inter 10'), fg='#ffffff',
    #                     border=0, cursor="hand2",command=lambda : example_add_function("3"))
    # appPriceBtn1.grid(column=3, row=3, sticky=S, pady=10)

    #Cart Body-----------------------------
    cartFrame = Frame(bodyFrame, bg="#101723")

    #Cart Frame BG
    cartBGLabel = Label(cartFrame, image=cartbg, bd=0, bg="#101723")
    cartBGLabel.place(x=0, y=0)

    #Cart Left Section Frame
    cartLeftFrame = Frame(cartFrame, bg="#192334", width=940, height=500)
    cartLeftFrame.pack(side=LEFT, expand=True, padx=(20,50), pady=10, anchor=W)

    cartLeftHeaderFrame = Frame(cartLeftFrame, bg="#192334")
    cartLeftHeaderFrame.pack(fill='both', pady=(0,5))

    cartLeftHeaderLabel = Label(cartLeftHeaderFrame, text="Your Item List", font=('Inter', 17), fg="white", bg="#192334", bd=1)
    cartLeftHeaderLabel.pack(side=LEFT)

    trashCanvasLabel = Canvas(cartLeftHeaderFrame, width=40, height=40, bg="#192334", highlightthickness=0, cursor="hand2")
    trashCanvasLabel.pack(anchor=E)
    trash_label = trashCanvasLabel.create_image((20,20), image=trash_icon)
    trashCanvasLabel.bind('<Button-1>', removeItem)

    graphCanvasLabel = Canvas(cartLeftHeaderFrame, width=40, height=40, bg="#192334", highlightthickness=0, cursor="hand2")
    graphCanvasLabel.pack(anchor=E)
    graph_label = graphCanvasLabel.create_image((20,20), image=graph_icon)
    graphCanvasLabel.bind('<Button-1>', showGraph)

    #Cart List/Record
    styleTree = ttk.Style()
    styleTree.theme_use('clam')
    styleTree.configure('Treeview.Heading', font=('Inter', 14, 'bold'), background="#304259", foreground="white", highlightthickness=0, bd=0, borderwidth=0)
    styleTree.configure('Treeview', font=('Inter', 13), background="#232F3E", foreground="white", highlightthickness=0, bd=0, fieldbackground="#232F3E", rowheight=30, lightcolor="#232F3E", darkcolor="#232F3E", bordercolor="#232F3E")
    styleTree.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})]) #Removes the borders

    styleTree.map("Treeview.Heading",
                    background = [('pressed', '!focus', "#304259"),
                                ('active', "#304259"),
                                ('disabled', '#304259')])

    columns = ("app_name", "app_price")
    tree = ttk.Treeview(cartLeftFrame, columns=columns, show='headings', height=15)
    tree.column("app_name", anchor=CENTER, stretch=NO, width=500)
    tree.heading("app_name", text="Application Name")
    tree.column("app_price",anchor=CENTER, stretch=NO, width=200)
    tree.heading("app_price", text="Price")
    tree.pack(anchor=W)

    def on_double_click(event):
        global selected_game_ids
        game_ids = []
        item = tree.selection()
        for i in item:
            game_id = tree.item(i, "values")[2]
            game_ids.append(game_id)

        selected_game_ids = game_ids


    tree.bind("<ButtonRelease-1>", on_double_click)

    def update_summary():
        balance = float(add_money.get_balance(add_money.get_misc_user()))

        yourFundsVar.set(str(round(balance, 2)))

        totalPayment = 0

        for game in get_users_cart_games(add_money.get_misc_user()):
            totalPayment += game["price"]

        totalPaymentVar.set(str(round(totalPayment, 2)))
        fundsLeft = balance - totalPayment;
        fundsLeftVar.set(str(round(fundsLeft, 2)))

        if fundsLeft >= 0:
            cartActualResultFundLabel.config(fg= "white")
            cartBuyButton.pack(anchor=E, pady=(30,0))
        else:
            cartActualResultFundLabel.config(fg= "red")
            cartBuyButton.pack_forget()






    #Sample List Data
    def update_item_list():
        for item in tree.get_children():
            tree.delete(item)

        index = 0
        for game in get_users_cart_games(add_money.get_misc_user()):
            tree.insert('', 'end', text=str(index + 1), values=(game["name"], game["price"], game["id"]))
            index += 1

        update_summary()

    # tree.insert('', 'end',text= "1",values=('Stardew Valley','419.95'))
    # tree.insert('', 'end',text= "2",values=('Wallpaper Engine', '135.95'))
    # tree.insert('', 'end',text= "3",values=('Kingdom Rush: Origins', '2,300.00'))
    # tree.insert('', 'end',text= "4",values=('Plaque Inc.', '301.46'))

    #Cart Right Section Frame
    cartRightFrame = Frame(cartFrame, bg="#192334", width=450)
    cartRightFrame.pack(side=RIGHT, fill='both', expand=True, padx=(0,50), pady=(47,20), anchor=E)

    cartSummaryLabel = Label(cartRightFrame, text="Summary", font=('Inter', 18), fg="white", bg="#192334")
    cartSummaryLabel.pack(anchor=W, pady=(60,20))

    cartDetailFrame = Frame(cartRightFrame, bg="#192334")
    cartDetailFrame.pack(fill=X, anchor=N)

    cartDetailLeftFrame = Frame(cartDetailFrame, bg="#192334")
    cartDetailLeftFrame.pack(side=LEFT, fill=X, padx=(0,80))


    cartCurrentFundLabel = Label(cartDetailLeftFrame, text="Your funds", font=('Inter', 12), fg="white", bg="#192334")
    cartCurrentFundLabel.pack(anchor=W, pady=(2,0))

    cartTotalLabel = Label(cartDetailLeftFrame, text="Total Payment", font=('Inter', 12), fg="white", bg="#192334")
    cartTotalLabel.pack(anchor=W, pady=(6,0))

    cartResultFundLabel = Label(cartDetailLeftFrame, text="Funds left", font=('Inter', 12), fg="white", bg="#192334")
    cartResultFundLabel.pack(anchor=W, pady=(20,0))

    cartDetailRightFrame = Frame(cartDetailFrame, bg="#192334")
    cartDetailRightFrame.pack(side=RIGHT, fill=X)

    yourFundsVar = StringVar()
    #Fund Label
    cartActualCurrentFundLabel = Label(cartDetailRightFrame, textvariable=yourFundsVar, font=('Inter', 15), fg="white", bg="#192334")
    cartActualCurrentFundLabel.pack(anchor=E)

    #Frame for the minus sign
    minusSignFrame = Frame(cartDetailRightFrame, bg="#192334")
    minusSignFrame.pack(anchor=E, pady=(3,3))

    minusCanvas = Canvas(minusSignFrame, height=1, width=10)
    minusCanvas.create_line(0,0,0,10, fill="white")
    minusCanvas.pack(side=LEFT, anchor=W, padx=(0, 84))

    totalPaymentVar = StringVar()
    #Total Label
    cartActualTotalLabel = Label(minusSignFrame, textvariable=totalPaymentVar, font=('Inter', 15), fg="white", bg="#192334")
    cartActualTotalLabel.pack(side=RIGHT, anchor=E)

    lineCanvas = Canvas(cartDetailRightFrame, height=1, width=175)
    lineCanvas.create_line(0,0,0,175, fill="white")
    lineCanvas.pack(anchor=E, pady=(3,3))

    #Funds Result Label
    fundsLeftVar = StringVar()
    cartActualResultFundLabel = Label(cartDetailRightFrame, textvariable=fundsLeftVar, font=('Inter', 15), fg="white", bg="#192334")
    cartActualResultFundLabel.pack(anchor=E)

    cartBuyButton = Button(cartRightFrame, text="Complete Transaction", font=('Inter', 12), fg="#101723", bg="white", bd=0, width=18, cursor="hand2", command=buyCart)
    cartBuyButton.pack(anchor=E, pady=(30,0))


    update_item_list()
    mainWindow.mainloop()
    
def nodef():
    main_login_screen.withdraw()
    top = Toplevel(main_login_screen)
    top.geometry("750x250")
    top.title("Child Window")
    Label(top, text="Example Window", font=('Mistral 18 bold')).place(x=150, y=80)


# Designing window for creating account
def remove_window():
        create_screen.destroy()
def createAccount():

    def change_state():
        if CheckTA.get() == 1:
            create_btn["state"] = "normal"
        else:
            create_btn["state"] = "disabled"


    global create_screen
    create_screen = Toplevel(main_login_screen)
    create_screen.title("Create Account")
    create_screen.geometry('400x250+570+230')
    create_screen.configure(bg="#192334")
    create_screen.resizable(False, False)
    create_screen.grab_set()

    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()

    Label(create_screen, text='Create Account', font=('Inter 15'), fg='#ffffff', bg="#192334").place(x=130, y=40)
    # create account
    #username
    username_label = Label(create_screen, text='Username', font=('Inter 12'), fg='#ffffff', bg='#192334')
    username_label.place(x=30, y=90)
    username_entry = Entry(create_screen, textvariable=username, width='23', fg='#000000', border=2, bg='#ffffff', font=('Inter 11'))
    username_entry.place(x=120, y=90)
    #passsword
    password_label = Label(create_screen, text='Password', font=('Inter 12'), fg='#ffffff', bg='#192334')
    password_label.place(x=30, y=130)
    password_entry = Entry(create_screen,textvariable= password, show='*', width='23', fg='#000000', border=2, bg='#ffffff', font=('Inter 11'))
    password_entry.place(x=120, y=130)

    #buttons- create and back

    create_btn = Button(create_screen, width=9, pady=1, text='Create', bg='#101723', font=('Inter 10'), fg='#ffffff',
                        border=0, cursor="hand2", state='disabled', command=create_user)
    create_btn.place(x=130, y=190)

    # login back to main screen
    Button(create_screen, width=9, pady=1, text='Back', bg='#ffffff', font=('Inter 10'), fg='#000000',
           border=0, cursor="hand2", command=remove_window).place(x=220, y=190)
    #terms and agreement
    CheckTA = IntVar()
    CheckTA.set(0)
    agreeCheck = Checkbutton(create_screen, bg='#192334', variable=CheckTA, onvalue=1, offvalue=0,
                                  text="I agree to terms and conditions",
                                  font=('Inter 8'), fg='#ffffff', activeforeground="#ffffff", activebackground="#192334",selectcolor="black", command=change_state).place(x=120, y=160)
"""
def create_user():

    username_info = username.get()
    password_info = password.get()
    
    if username_info == "" or password_info == "":
        return
    else:
        file = open(username_info, "w")
        file.write(username_info + "\n")
        file.write(password_info)
        file.close()

    username_entry.delete(0, END)
    password_entry.delete(0, END)

    create_screen.destroy()
    pop_up_screen = Toplevel(main_login_screen)
    pop_up_screen.title("")
    pop_up_screen.geometry('200x100+660+300')
    pop_up_screen.configure(bg="#192334")
    pop_up_screen.resizable(False, False)

    Label(pop_up_screen, text="Registration Success!", font=('Inter 10'), fg='#ffffff', bg="#192334").place(x=30, y=15)
    Button(pop_up_screen, width=9, pady=1, text='OK', bg='#101723', font=('Inter 10'), fg='#ffffff',
                        border=0, cursor="hand2", command=lambda: pop_up_screen.destroy()).place(x=60, y=50)
    """

# Create a connection to the database and a cursor object
conn = sqlite3.connect('appstore.db')
c = conn.cursor()

# Create a table named 'users' with columns 'username' and 'password'
c.execute('''CREATE TABLE IF NOT EXISTS users
             (username TEXT, password TEXT)''')
conn.commit()

def create_user():
    username_info = username.get()
    password_info = password.get()

    # Checking the empty fields
    if not username_info or not password_info:
        messagebox.showwarning('Empty Field', 'Fill all the fields')
        return

    # Insert the new user's username and password into the 'users' table
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username_info, password_info))
    conn.commit()

    username_entry.delete(0, END)
    password_entry.delete(0, END)

    create_screen.destroy()
    pop_up_screen = Toplevel(main_login_screen)
    pop_up_screen.title("")
    pop_up_screen.geometry('200x100+660+300')
    pop_up_screen.configure(bg="#192334")
    pop_up_screen.resizable(False, False)
    Label(pop_up_screen, text="Registration Success!", font=('Inter 10'), fg='#ffffff', bg="#192334").place(x=30, y=15)
    Button(pop_up_screen, width=9, pady=1, text='OK', bg='#101723', font=('Inter 10'), fg='#ffffff', cursor="hand2", command=pop_up_screen.destroy).place(x=60, y=50)

# designframe for login account window
def loginFrame1():
    # frame1 design (left)
    Frame(main_login_screen, bg="#101723", height='310', width='279').pack(side=LEFT)


    # system title, motto, and version
    Label(main_login_screen, text='EaseBuy App Store', font=('Inter 10'), fg='#ffffff', bg='#101723').place(x=120, y=50)

    Label(main_login_screen,
                         text='“Some cheesy line or motto \n or vision or whatever idk here \n extra string to make it 3 line” \n ',
                         font=('Inter 8 italic'), justify="left", fg='#ffffff', bg='#101723').place(x=60, y=150)

    Label(main_login_screen, text='version 0.00.01', font=('Inter 10'), fg='#ffffff', bg='#101723').place(x=90, y=280)


def loginFrame2():
    # frame 2 design (right)
    heading = Label(main_login_screen, text='Login Account', font=('Inter 15'), fg='#ffffff', bg="#192334")
    heading.place(x=300, y=50)

    global username_verify
    global password_verify
    global username_login_entry
    global password_login_entry

    username_verify = StringVar()
    password_verify = StringVar()

    # Username label and entry
    username = Label(main_login_screen, text='Username', font=('Inter 10'), fg='#ffffff', bg='#192334')
    username.place(x=300, y=110)
    username_login_entry = Entry(main_login_screen, textvariable=username_verify, width='23', fg='#000000', border=2, bg='#ffffff', font=('Inter 11'))
    username_login_entry.place(x=380, y=110)

    # password label and entry
    password = Label(main_login_screen, text='Password', font=('Inter 10'), fg='#ffffff', bg='#192334')
    password.place(x=300, y=160)
    password_login_entry = Entry(main_login_screen, show='*', textvariable=password_verify, width='23', fg='#000000', border=2, bg='#ffffff', font=('Inter 11'))
    password_login_entry.place(x=380, y=160)

def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()

    temp_user = username1

    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)

    # Query the 'users' table for the username and password
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username1, password1))
    result = c.fetchone()
    if result:
        add_money.save_misc_user(temp_user)
        login_success()
    else:
        user_not_found()

# Close the database connection when the program exits
def on_exit():
    conn.close()
    main_login_screen.destroy()


# Designing popup for login success -----> Jumping or integrating to the main window of the system
def login_success():
    def go_to_main_app():
        
        user_not_found_screen.destroy()
        main_login_screen.destroy()

        # initialize balance of no balance users
        add_money.initialize_user_balance()

        main_app()
        
    
    global user_not_found_screen
    user_not_found_screen = Toplevel(main_login_screen)
    user_not_found_screen.title("")
    user_not_found_screen.geometry('200x100+660+300')
    user_not_found_screen.configure(bg="#192334")
    user_not_found_screen.resizable(False, False)

    Label(user_not_found_screen, text="Login Success!", font=('Inter 10'), fg='#ffffff', bg="#192334").place(x=45, y=15)
    Button(user_not_found_screen, width=9, pady=1, text='OK', bg='#101723', font=('Inter 10'), fg='#ffffff',
           border=0, cursor="hand2", command=go_to_main_app).place(x=60, y=50)


# Designing popup for login invalid password

def password_not_recognised():
    global user_not_found_screen
    user_not_found_screen = Toplevel(main_login_screen)
    user_not_found_screen.title("")
    user_not_found_screen.geometry('200x100+660+300')
    user_not_found_screen.configure(bg="#192334")
    user_not_found_screen.resizable(False, False)

    Label(user_not_found_screen, text="Invalid Password!", font=('Inter 10'), fg='#ffffff', bg="#192334").place(x=40, y=15)
    Button(user_not_found_screen, width=9, pady=1, text='OK', bg='#101723', font=('Inter 10'), fg='#ffffff',
           border=0, cursor="hand2", command=lambda: user_not_found_screen.destroy()).place(x=60, y=50)


# Designing popup for user not found

def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(main_login_screen)
    user_not_found_screen.title("")
    user_not_found_screen.geometry('200x100+660+300')
    user_not_found_screen.configure(bg="#192334")
    user_not_found_screen.resizable(False, False)

    Label(user_not_found_screen, text="User Not Found", font=('Inter 10'), fg='#ffffff', bg="#192334").place(
        x=40, y=15)
    Button(user_not_found_screen, width=9, pady=1, text='OK', bg='#101723', font=('Inter 10'), fg='#ffffff',
           border=0, cursor="hand2", command=lambda: user_not_found_screen.destroy()).place(x=60, y=50)

# Deleting popups - gumamit na lang ako lambda para mas short ang coding pero baka magamit sa back end toh
"""
def delete_login_success():
    user_not_found_screen.destroy()


def delete_password_not_recognised():
    user_not_found_screen.destroy()


def delete_user_not_found_screen():
    user_not_found_screen.destroy()
"""
# create a login window
def main_account_screen():

    global main_login_screen
    main_login_screen = Tk()
    main_login_screen.title('Login')
    main_login_screen.geometry('637x309+450+200')
    main_login_screen.configure(bg="#192334")
    main_login_screen.resizable(False, False)

    #global Font
    #Font(file="Inter-Regular.ttf", family="Inter")
    loginFrame1()
    loginFrame2()


    # button for login
    login_btn = Button(main_login_screen, width=9, pady=1, text='Login', bg='#ffffff', font=('Inter 10'), fg='#000000',
                       border=0, cursor="hand2", command=login_verify)
    login_btn.place(x=390, y=220)

    # button for create
    Button(main_login_screen, width=9, pady=1, text='Create', bg='#101723', font=('Inter 10'), fg='#ffffff',
                        border=0, cursor="hand2", command=createAccount).place(x=480, y=220)

    main_login_screen.mainloop()

main_account_screen()
