import random

# ------------------------ Generate Error Function -----------------------------
def generate_error(err_type, isSilly=False):
    if not isSilly:
        if err_type == "syntax":
            return "SyntaxError: unexpected EOF while parsing"
        
        if err_type == "runtime":
            return "NameError: name 'undefined_variable' is not defined"
        
        if err_type == "logical":
            return "In JavaScript 0+1 == True"
    
    else:
        if err_type == "syntax":
            return "SINNNNNtaxError: unexpected EOF while parsing HEHE"
        
        if err_type == "runtime":
            return "NAMEMEMEMEError: HEHEHAHA name 'undefined_variable' is not defined"
        
        if err_type == "logical":
            return "THE LOGIC IS NOT RIGHT"
        
# ------------------------ End of Generate Error Function-----------------------------

# ------------------------ Hacked Message Generator Code -----------------------------
silly_hackers = ["potato", "robot", "friendly alien", "unicorn", "talking toaster"]
silly_hacker_names = ["Potato Inc.", "Elon Musk", "Zog the Alien", "Fluffy the Unicorn", "slurp-slurp"]
silly_computer_entities = ["laptop", "fridge", "smartphone", "toilet", "coffee maker"]

# Define the generate_hacked_message function
def generate_hacked_message(is_long=False, is_silly=False):
    hacked_messages = []

    for _ in range(5 if is_long else 1):
        if is_silly:
            hacker = random.choice(silly_hackers)
            hacker_name = random.choice(silly_hacker_names)
            computer_entity = random.choice(silly_computer_entities)
            message = f"Warning! Your {computer_entity} has been hacked by a {hacker}."
            message += f"\n  - Hacked by: {hacker_name}"
            message += f"\n  - Hacking ID: {random.randint(10000, 99999)}"
        else:
            # Generate a standard hacked message
            message = f"Warning! Your computer has been hacked by an anonymous hacker."
            message += f"\n  - Hacker ID: {random.randint(10000, 99999)}"
            message += f"\n  - Hacking Timestamp: {random.randint(1, 12)}:{random.randint(0, 59)} AM"

        hacked_messages.append(message)

    return hacked_messages

# ------------------------ End of Hacked Message Generator Code -----------------------------


# ------------------------ Stack Trace Generator Code -----------------------------
def generate_stacktrace(length = 0, is_silly=False):
    short = "Traceback (most recent call last):\n  File \"\\Users\\pyperror\\utils\\migration_utils.py\", line 887, in <module>\n    is_approved = calculate_triangle_area(user_responses)\n  File \"\\Users\\pyperror\\api\\product_api.py\", line 487, in calculate_triangle_area\n    is_approved = validate_user_age(word_count)\n  File \"\\Users\\pyperror\\config\\email_config.py\", line 630, in validate_user_age\n    credit_card_number = validate_product_code(order_status)\nTypeError: unsupported operand type(s) for +: 'int' and 'str'"
    long = "Traceback (most recent call last):\n  File \"\\Users\\pyperror\\models\\category_model.py\", line 998, in <module>\n    reviewer_name = validate_user_age(is_verified)\n  File \"\\Users\\pyperror\\config\\api_config.py\", line 13, in validate_user_age\n    product_rating = validate_phone_number(survey_results)\n  File \"\\Users\\pyperror\\scripts\\data_processing.py\", line 518, in validate_phone_number\n    workshop_duration = process_data(first_name)\n  File \"\\Users\\pyperror\\config\\migration_config.py\", line 536, in process_data\n    attendee_name = generate_transaction_id(workshop_name)\n  File \"\\Users\\pyperror\\utils\\security_utils.py\", line 167, in generate_transaction_id\n    page_count = format_currency(manufacturing_date)\n  File \"\\Users\\pyperror\\utils\\validation_utils.py\", line 176, in format_currency\n    is_in_stock = generate_signature(product_rating)\n  File \"\\Users\\pyperror\\tests\\test_security.py\", line 370, in generate_signature\n    conference_name = send_push_notification(publication_date)\n  File \"\\Users\\pyperror\\tests\\test_api.py\", line 60, in send_push_notification\n    email_address = fetch_data_from_api(product_name)\n  File \"\\Users\\pyperror\\api\\invoice_api.py\", line 850, in fetch_data_from_api\n    event_capacity = check_user_permissions(is_deleted)\n  File \"\\Users\\pyperror\\views\\invoice_view.py\", line 562, in check_user_permissions\n    workshop_name = parse_config_file(response_value)\n  File \"\\Users\\pyperror\\tests\\test_user_management.py\", line 478, in parse_config_file\n    quantity = generate_api_key(price)\n  File \"\\Users\\pyperror\\config\\api_config.py\", line 916, in generate_api_key\n    event_location = parse_binary_data(ticket_price)\n  File \"\\Users\\pyperror\\views\\notification_view.py\", line 103, in parse_binary_data\n    workshop_duration = parse_sensor_signals(publication_date)\nNameError: name 'response_text' is not defined"       
    shortfunny = "Traceback (most recent call last):\n  File \"\\Users\\pyperror\\utils\\string_operations.py\", line 709, in <module>\n    chocolate_rain = predictFuture(starbucks_coffee)\n  File \"\\Users\\pyperror\\tests\\test_models.py\", line 716, in predictFuture\n    gummybearxd = countSheepUntilSleep(lasagna_layers)\n  File \"\\Users\\pyperror\\api\\authentication_api.py\", line 213, in countSheepUntilSleep\n    michael_jackson = confuseCats(jellybeans)\nAttributeError: 'list' object has no attribute 'appendx'"
    longfunny = "Traceback (most recent call last):\n  File \"\\Users\\pyperror\\views\\invoice_view.py\", line 58, in <module>\n    elonmusk = transformIntoAPumpkin(michael_jackson)\n  File \"\\Users\\pyperror\\scripts\\report_generation.py\", line 495, in transformIntoAPumpkin\n    bananas = findMeaningOfLife(joe_biden)\n  File \"\\Users\\pyperror\\config\\config_parser.py\", line 393, in findMeaningOfLife\n    unicorn_num = countSheepUntilSleep(michael_jackson)\n  File \"\\Users\\pyperror\\utils\\migration_utils.py\", line 365, in countSheepUntilSleep\n    gummybearxd = transformIntoAPumpkin(jellybeans)\n  File \"\\Users\\pyperror\\utils\\email_utils.py\", line 657, in transformIntoAPumpkin\n    chocolate_rain = speakInDolphin(lasagna_layers)\n  File \"\\Users\\pyperror\\scripts\\data_migration.py\", line 962, in speakInDolphin\n    spiderman_weblength = brewMagicPotion(minecraft)\n  File \"\\Users\\pyperror\\tests\\test_security.py\", line 923, in brewMagicPotion\n    starbucks_coffee = danceLikeNoOneIsWatching(lasagna_layers)\n  File \"\\Users\\pyperror\\controllers\\supplier_controller.py\", line 735, in danceLikeNoOneIsWatching\n    toiletPaper_Length = createUniverse(bobby_shmurda)\n  File \"\\Users\\pyperror\\views\\profile_view.py\", line 780, in createUniverse\n    toiletPaper_Length = teleportToMars(starbucks_coffee)\n  File \"\\Users\\pyperror\\scripts\\data_processing.py\", line 670, in teleportToMars\n    joe_biden = confuseCats(jellybeans)\n  File \"\\Users\\pyperror\\tests\\test_utils.py\", line 828, in confuseCats\n    jellybeans = predictFuture(starbucks_coffee)\n  File \"\\Users\\pyperror\\tests\\test_import.py\", line 896, in predictFuture\n    michael_jackson = predictFuture(chocolate_rain)\nKeyError: 'option3'"


    if length == 0:
        if is_silly == False:
            print(short)
        elif is_silly == True:
            print(shortfunny)
    elif length == 1:
        if is_silly == False:
            print(long)
        elif is_silly == True:
            print(longfunny)

short = "Traceback (most recent call last):\n  File \"\\Users\\pyperror\\utils\\migration_utils.py\", line 887, in <module>\n    is_approved = calculate_triangle_area(user_responses)\n  File \"\\Users\\pyperror\\api\\product_api.py\", line 487, in calculate_triangle_area\n    is_approved = validate_user_age(word_count)\n  File \"\\Users\\pyperror\\config\\email_config.py\", line 630, in validate_user_age\n    credit_card_number = validate_product_code(order_status)\nTypeError: unsupported operand type(s) for +: 'int' and 'str'"
long = "Traceback (most recent call last):\n  File \"\\Users\\pyperror\\models\\category_model.py\", line 998, in <module>\n    reviewer_name = validate_user_age(is_verified)\n  File \"\\Users\\pyperror\\config\\api_config.py\", line 13, in validate_user_age\n    product_rating = validate_phone_number(survey_results)\n  File \"\\Users\\pyperror\\scripts\\data_processing.py\", line 518, in validate_phone_number\n    workshop_duration = process_data(first_name)\n  File \"\\Users\\pyperror\\config\\migration_config.py\", line 536, in process_data\n    attendee_name = generate_transaction_id(workshop_name)\n  File \"\\Users\\pyperror\\utils\\security_utils.py\", line 167, in generate_transaction_id\n    page_count = format_currency(manufacturing_date)\n  File \"\\Users\\pyperror\\utils\\validation_utils.py\", line 176, in format_currency\n    is_in_stock = generate_signature(product_rating)\n  File \"\\Users\\pyperror\\tests\\test_security.py\", line 370, in generate_signature\n    conference_name = send_push_notification(publication_date)\n  File \"\\Users\\pyperror\\tests\\test_api.py\", line 60, in send_push_notification\n    email_address = fetch_data_from_api(product_name)\n  File \"\\Users\\pyperror\\api\\invoice_api.py\", line 850, in fetch_data_from_api\n    event_capacity = check_user_permissions(is_deleted)\n  File \"\\Users\\pyperror\\views\\invoice_view.py\", line 562, in check_user_permissions\n    workshop_name = parse_config_file(response_value)\n  File \"\\Users\\pyperror\\tests\\test_user_management.py\", line 478, in parse_config_file\n    quantity = generate_api_key(price)\n  File \"\\Users\\pyperror\\config\\api_config.py\", line 916, in generate_api_key\n    event_location = parse_binary_data(ticket_price)\n  File \"\\Users\\pyperror\\views\\notification_view.py\", line 103, in parse_binary_data\n    workshop_duration = parse_sensor_signals(publication_date)\nNameError: name 'response_text' is not defined"       
shortfunny = "Traceback (most recent call last):\n  File \"\\Users\\pyperror\\utils\\string_operations.py\", line 709, in <module>\n    chocolate_rain = predictFuture(starbucks_coffee)\n  File \"\\Users\\pyperror\\tests\\test_models.py\", line 716, in predictFuture\n    gummybearxd = countSheepUntilSleep(lasagna_layers)\n  File \"\\Users\\pyperror\\api\\authentication_api.py\", line 213, in countSheepUntilSleep\n    michael_jackson = confuseCats(jellybeans)\nAttributeError: 'list' object has no attribute 'appendx'"
longfunny = "Traceback (most recent call last):\n  File \"\\Users\\pyperror\\views\\invoice_view.py\", line 58, in <module>\n    elonmusk = transformIntoAPumpkin(michael_jackson)\n  File \"\\Users\\pyperror\\scripts\\report_generation.py\", line 495, in transformIntoAPumpkin\n    bananas = findMeaningOfLife(joe_biden)\n  File \"\\Users\\pyperror\\config\\config_parser.py\", line 393, in findMeaningOfLife\n    unicorn_num = countSheepUntilSleep(michael_jackson)\n  File \"\\Users\\pyperror\\utils\\migration_utils.py\", line 365, in countSheepUntilSleep\n    gummybearxd = transformIntoAPumpkin(jellybeans)\n  File \"\\Users\\pyperror\\utils\\email_utils.py\", line 657, in transformIntoAPumpkin\n    chocolate_rain = speakInDolphin(lasagna_layers)\n  File \"\\Users\\pyperror\\scripts\\data_migration.py\", line 962, in speakInDolphin\n    spiderman_weblength = brewMagicPotion(minecraft)\n  File \"\\Users\\pyperror\\tests\\test_security.py\", line 923, in brewMagicPotion\n    starbucks_coffee = danceLikeNoOneIsWatching(lasagna_layers)\n  File \"\\Users\\pyperror\\controllers\\supplier_controller.py\", line 735, in danceLikeNoOneIsWatching\n    toiletPaper_Length = createUniverse(bobby_shmurda)\n  File \"\\Users\\pyperror\\views\\profile_view.py\", line 780, in createUniverse\n    toiletPaper_Length = teleportToMars(starbucks_coffee)\n  File \"\\Users\\pyperror\\scripts\\data_processing.py\", line 670, in teleportToMars\n    joe_biden = confuseCats(jellybeans)\n  File \"\\Users\\pyperror\\tests\\test_utils.py\", line 828, in confuseCats\n    jellybeans = predictFuture(starbucks_coffee)\n  File \"\\Users\\pyperror\\tests\\test_import.py\", line 896, in predictFuture\n    michael_jackson = predictFuture(chocolate_rain)\nKeyError: 'option3'"
# ------------------------ End of Stack Trace Generator Code -----------------------------

# ------------------------- Crash Report Generator Code ---------------------------
def generate_crash_report(is_long=False, is_silly=False):
    random_number = random.randint(0, 4)
    if is_silly:
        if is_long:
            print(silly_long)
        else:
            print(silly_short)
    else: # not silly
        if is_long:
            print(long[random_number])
        else:
            print(short[random_number])

silly_short = """CRASH REPORT: App experienced "exhausted of running everyday with bugs" error and gave up trying while user juggled watermelons."""

silly_long = """CRASH REPORT:
Exception Type: App Fatigue Exception
Message: App exhausted from running tirelessly.

App Details:
- App Name: WearyWorker.exe
- Version: 3.2.0
- Last Seen: Somewhere in the distant past

App's Final Words: "I'm taking a nap now."

Reason for Exhaustion:
- Ran endless errands and never complained.
- Processed more data than a supercomputer.

Recommendation:
- Provide a cozy blanket and a cup of virtual hot cocoa.

Report Id: 42-REST"""

s1 = "Faulting application name: systemProtect.exe, version: 3.0.2.4, faulting module name: ntdll.dll, exception code: 0xc0000005"
s2 = "UNEXPECTED_KERNEL_MODE_TRAP"
s3 = "Kernel panic - not syncing: Attempted to kill init!"
s4 = "Stop 0x0000007B: INACCESSIBLE_BOOT_DEVICE"
s5 = ":( your pc ran into a problem and needs to restart loop"

short = [s1, s2, s3, s4, s5]

l1 = """Process:               com.symantec.SymLUHelper [25336]
Path:                  /Library/Application Support/Symantec/*/com.symantec.SymLUHelper
Identifier:            com.symantec.SymLUHelper
Version:               ???
Code Type:             X86-64 (Translated)
Parent Process:        launchd [1]
User ID:               0

Date/Time:             2023-11-02 20:12:45.8451 -0400
OS Version:            macOS 12.1 (21C52)
Report Version:        12
Anonymous UUID:        D6567CFE-1FBF-D9F7-8EA2-67A9701AAE6F

Sleep/Wake UUID:       2D1AAE05-AD7A-4DC8-8A92-DE89FF7F326F

Time Awake Since Boot: 210000 seconds
Time Since Wake:       2277 seconds

System Integrity Protection: enabled

Notes:
thread_get_state(PAGEIN) returned 0x10000003: (ipc/send) invalid destination port
thread_get_state(EXCEPTION) returned 0x10000003: (ipc/send) invalid destination port
thread_get_state(FLAVOR) returned 0x10000003: (ipc/send) invalid destination port

Crashed Thread:        3  Dispatch queue: com.apple.main-thread

Exception Type:        EXC_BAD_INSTRUCTION (SIGILL)
Exception Codes:       0x0000000000000001, 0x0000000000000000
Exception Note:        EXC_CORPSE_NOTIFY

Termination Reason:    Namespace SIGNAL, Code 4 Illegal instruction: 4
Terminating Process:   exc handler [25336]

Application Specific Information:
XPC API Misuse: Array mutated during iteration


Application Specific Signatures:
API Misuse"""

l2 = """CRASH REPORT:
Exception Type: Segmentation fault
Message: Process terminated with signal 11 (Segmentation fault)

Memory Dump:
Address    Data
0x00000000 0x00000000
0x00000004 0x12345678
0x00000008 0x00000001
0x0000000C 0x87654321
0x00000010 0xDEADBEEF
0x00000014 0xCAFEBABE
0x00000018 0x7E7E7E7E
0x0000001C 0x01234567
0x00000020 0xABCDEF12
0x00000024 0x98765432
...
0x7FFFFFFC 0x12345678
0x7FFFFFDC 0x55555555
0x7FFFFFE0 0xAAAAAAAA
0x7FFFFFE4 0xBBBBBBBB
0x7FFFFFE8 0xCCCCCCCC
0x7FFFFFEC 0xDDDDDDDD"""

l3 = r"""Log Name: Application
Source: Application Error
Date: 2023-11-02 14:30:45
Event ID: 1001
Task Category: Application Crashing Events
Level: Error
Keywords: Classic
User: N/A
Computer: Admin
Description:
Faulting application name: SystemUpdate.exe, version: 1.0.0.0, time stamp: 0x5a65739b
Faulting module name: ntdll.dll, version: 10.0.19041.662, time stamp: 0xef4551e9
Exception code: 0xc0000005
Fault offset: 0x00000000000489e8
Faulting process id: 0x13f8
Faulting application start time: 0x01d6bd21c70060b4
Faulting application path: C:\Path\To\SystemUpdate.exe
Faulting module path: C:\Windows\SYSTEM32\ntdll.dll
Report Id: 0d5e238d-85b7-4b41-9681-1cf64cbe2d4e
Faulting package full name: 
Faulting package-relative application ID: 
Event Xml:
<Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event">
  <System>
    <Provider Name="Application Error" />
    <EventID Qualifiers="0">1000</EventID>
    <Level>2</Level>
    <Task>100</Task>
    <Keywords>0x80000000000000</Keywords>
    <TimeCreated SystemTime="2023-11-02T14:30:45.524272300Z" />
    <EventRecordID>0517</EventRecordID>
    <Channel>Application</Channel>
    <Computer>Admin</Computer>
    <Security />
  </System>
</Event>"""

l4 = """Process:               bird [1601]
Path:                  /System/Library/PrivateFrameworks/CloudDocsDaemon.framework/Versions/A/Support/bird
Identifier:            bird
Version:               321.6
Code Type:             X86-64 (Native)
Parent Process:        ??? [1]
Responsible:           bird [1601]
User ID:               501

Date/Time:             2016-08-01 13:11:55.824 +0800
OS Version:            Mac OS X 10.10.3 (14D136)
Report Version:        11
Anonymous UUID:        78513341-BC61-B7B5-7704-922A48CC563E

Sleep/Wake UUID:       332B8005-A48E-4395-A9C5-8D47648E897C

Time Awake Since Boot: 36000 seconds
Time Since Wake:       4100 seconds

Crashed Thread:        0  Dispatch queue: com.apple.sqlite.clientTruth

Exception Type:        EXC_CRASH (SIGABRT)
Exception Codes:       0x0000000000000000, 0x0000000000000000

Application Specific Information:
*** Terminating app due to uncaught exception 'NSInternalInconsistencyException', reason: 'Sqlite rollbacked transaction [<PQLStatement:0x7fc8d075f890 {commit}>] because of unrecoverable error [Error Domain=SqliteErrorDomain Code=13 "未能完成该操作。（SqliteErrorDomain 错误 13 - database or disk is full）" UserInfo=0x7fc8d067a9b0 {SqliteSQL=commit, SqliteExtendedCode=13, NSDescription=database or disk is full, NSUnderlyingError=0x7fc8d0678260 "未能完成该操作。设备上无剩余空间"}], aborting.'
terminating with uncaught exception of type NSException
abort() called"""

l5 = """A problem has been detected and windows has been shut down to prevent damage
to your computer.

The problem seems to be caused by the following file: SPCMDCON. SYS

PAGE_FAULT_IN_NONPAGED_AREA

If this is the first time you've seen this stop error screen,
restart your computer. If this screen appears again, follow
these steps:

Check to make sure any new hardware or software is properly installed.
If this is a new installation, ask your hardware or software manufacturer
for any windows updates you might need.

If problems continue, disable or remove any newly installed hardware
or software. Disable BIOS memory options such as caching or shadowing.
If you need to use Safe Mode to remove or disable components, restart
your computer, press F8 to select Advanced startup options, and then
select Safe Mode.

Technical information:

*** STOP: 0x00000050 (OXFD3094C2, 0x00000001, 0xFBFE7617, 0x00000000)


SPCMDCON. SYS - Address FBFE7617 base at FBFE5000, Datestamp 3d6dd67c"""

long = [l1, l2, l3, l4, l5]
is_long = True
is_silly = True

