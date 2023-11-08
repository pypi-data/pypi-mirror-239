import random
# some useless comments to trigger changes. TO DELETE
# some useless comments to trigger changes. TO DELETE
# some useless comments to trigger changes. TO DELETE
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
API Misuse

Error Formulating Crash Report:
thread_get_state(PAGEIN) returned 0x10000003: (ipc/send) invalid destination port
thread_get_state(EXCEPTION) returned 0x10000003: (ipc/send) invalid destination port
thread_get_state(FLAVOR) returned 0x10000003: (ipc/send) invalid destination port

Thread 0:: com.apple.rosetta.exceptionserver
0   runtime                       	    0x7ff7ffcb18e4 0x7ff7ffcad000 + 18660
1   runtime                       	    0x7ff7ffcbe928 0x7ff7ffcad000 + 71976
2   runtime                       	    0x7ff7ffcc00a4 0x7ff7ffcad000 + 77988

Thread 1::  Dispatch queue: symtrace-monitor
0   ???                           	    0x7ff8a47f6940 ???
1   libsystem_kernel.dylib        	    0x7ff81423caba mach_msg_trap + 10
2   CoreFoundation                	    0x7ff81433fdf1 __CFRunLoopServiceMachPort + 319
3   CoreFoundation                	    0x7ff81433e4af __CFRunLoopRun + 1329
4   CoreFoundation                	    0x7ff81433d8a9 CFRunLoopRunSpecific + 567
5   CoreFoundation                	    0x7ff8143c4e66 CFRunLoopRun + 40
6   SymBase                       	       0x10d83ddd6 0x10d81c000 + 138710
7   libdispatch.dylib             	    0x7ff8140bead8 _dispatch_call_block_and_release + 12
8   libdispatch.dylib             	    0x7ff8140bfcc9 _dispatch_client_callout + 8
9   libdispatch.dylib             	    0x7ff8140c5e0f _dispatch_lane_serial_drain + 985
10  libdispatch.dylib             	    0x7ff8140c67c8 _dispatch_lane_invoke + 366
11  libdispatch.dylib             	    0x7ff8140d07e1 _dispatch_workloop_worker_thread + 758
12  libsystem_pthread.dylib       	    0x7ff814276074 _pthread_wqthread + 326
13  libsystem_pthread.dylib       	    0x7ff814274ffb start_wqthread + 15

Thread 2:
0   runtime                       	    0x7ff7ffccf814 0x7ff7ffcad000 + 141332

Thread 3 Crashed::  Dispatch queue: com.apple.main-thread
0   libxpc.dylib                  	    0x7ff813fcfb82 _xpc_api_misuse + 117
1   libxpc.dylib                  	    0x7ff813fbaab0 xpc_array_apply + 110
2   com.symantec.SymLUHelper      	       0x104c36bb2 0x104c2e000 + 35762
3   libdispatch.dylib             	    0x7ff8140bfcc9 _dispatch_client_callout + 8
4   libdispatch.dylib             	    0x7ff8140c2746 _dispatch_continuation_pop + 460
5   libdispatch.dylib             	    0x7ff8140d3a5a _dispatch_source_invoke + 2150
6   libdispatch.dylib             	    0x7ff8140c5b85 _dispatch_lane_serial_drain + 335
7   libdispatch.dylib             	    0x7ff8140c67fb _dispatch_lane_invoke + 417
8   libdispatch.dylib             	    0x7ff8140c226d _dispatch_queue_override_invoke + 463
9   libdispatch.dylib             	    0x7ff8140cf3ba _dispatch_root_queue_drain + 343
10  libdispatch.dylib             	    0x7ff8140cfb5a _dispatch_worker_thread2 + 160
11  libsystem_pthread.dylib       	    0x7ff81427602e _pthread_wqthread + 256
12  libsystem_pthread.dylib       	    0x7ff814274ffb start_wqthread + 15

Thread 4:
0   ???                           	    0x7ff8a47f6940 ???
1   libsystem_kernel.dylib        	    0x7ff81423caba mach_msg_trap + 10
2   SymQual                       	       0x10db978e8 0x10db86000 + 71912
3   libsystem_pthread.dylib       	    0x7ff8142794f4 _pthread_start + 125
4   libsystem_pthread.dylib       	    0x7ff81427500f thread_start + 15

Thread 5:
0   ???                           	    0x7ff8a47f6940 ???
1   libsystem_kernel.dylib        	    0x7ff8142422e2 __sigsuspend_nocancel + 10
2   libdispatch.dylib             	    0x7ff8140d10da _dispatch_sig_thread + 53

Thread 6:
0   runtime                       	    0x7ff7ffccf814 0x7ff7ffcad000 + 141332


No thread state (register information) available

Binary Images:
    0x7ff7ffcad000 -     0x7ff7ffcdcfff runtime (*) <21c1e0c9-a36e-3e4b-a12b-1bf54ce4403e> /usr/libexec/rosetta/runtime
               0x0 - 0xffffffffffffffff ??? (*) <00000000-0000-0000-0000-000000000000> ???
    0x7ff81423c000 -     0x7ff814272fff libsystem_kernel.dylib (*) <5aa1e5be-b5b8-3a02-9885-a8c99e0ca378> /usr/lib/system/libsystem_kernel.dylib
    0x7ff8142c0000 -     0x7ff8147c0fff com.apple.CoreFoundation (6.9) <7e1d1901-3f9e-3e2e-a090-3655e5f5e04b> /System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation
       0x10d81c000 -        0x10d86dfff com.symantec.symbase (14.2) <f8be5112-b81a-36f8-92c8-cc8d50c60624> /Library/Application Support/Symantec/*/SymBase.framework/Versions/B/SymBase
    0x7ff8140bd000 -     0x7ff814103fff libdispatch.dylib (*) <c8f7bfb6-4b1a-37cd-a32d-cd5069c916df> /usr/lib/system/libdispatch.dylib
    0x7ff814273000 -     0x7ff81427efff libsystem_pthread.dylib (*) <6c7561b4-4b92-3f45-921e-abe669299844> /usr/lib/system/libsystem_pthread.dylib
    0x7ff813fae000 -     0x7ff813fe4fff libxpc.dylib (*) <43dadc38-d163-3eef-8901-0cbce39c7cc5> /usr/lib/system/libxpc.dylib
       0x104c2e000 -        0x104c60fff com.symantec.SymLUHelper (*) <42a3c887-4f11-3561-b0e0-e3d102ac7e5d> /Library/Application Support/Symantec/*/com.symantec.SymLUHelper
       0x10db86000 -        0x10dccafff com.symantec.symqual.framework (14.2) <c603268b-828d-3615-8f02-a2226c38cdf0> /Library/Application Support/Symantec/*/SymQual.framework/Versions/A/SymQual

External Modification Summary:
  Calls made by other processes targeting this process:
    task_for_pid: 0
    thread_create: 0
    thread_set_state: 0
  Calls made by this process:
    task_for_pid: 0
    thread_create: 0
    thread_set_state: 0
  Calls made by all processes on this machine:
    task_for_pid: 0
    thread_create: 0
    thread_set_state: 0

VM Region Summary:
ReadOnly portion of Libraries: Total=1.1G resident=0K(0%) swapped_out_or_unallocated=1.1G(100%)
Writable regions: Total=1.5G written=0K(0%) resident=0K(0%) swapped_out=0K(0%) unallocated=1.5G(100%)

                                VIRTUAL   REGION 
REGION TYPE                        SIZE    COUNT (non-coalesced) 
===========                     =======  ======= 
Activity Tracing                   256K        1 
Kernel Alloc Once                    8K        1 
MALLOC                           377.6M       46 
MALLOC guard page                   96K        6 
MALLOC_MEDIUM (reserved)         584.0M        6         reserved VM address space (unallocated)
MALLOC_NANO (reserved)           384.0M        1         reserved VM address space (unallocated)
Rosetta Arena                     4096K        2 
Rosetta Generic                   1660K      412 
Rosetta IndirectBranch             256K        1 
Rosetta JIT                      128.0M        1 
Rosetta Return Stack               100K       10 
Rosetta Thread Context             100K       10 
SQLite page cache                  256K        4 
STACK GUARD                          8K        2 
Stack                             3176K        7 
Stack Guard                       64.0M        6 
VM_ALLOCATE                       6968K       21 
__DATA                            24.1M      447 
__DATA_CONST                      25.6M      272 
__DATA_DIRTY                      1421K      174 
__FONT_DATA                          4K        1 
__LINKEDIT                       703.9M       25 
__OBJC_RO                         81.8M        1 
__OBJC_RW                         3136K        2 
__TEXT                           426.3M      461 
__UNICODE                          588K        1 
dyld private memory               1056K        3 
mapped file                        4.8G      756 
shared memory                      612K        6 
unshared pmap                     6720K        4 
===========                     =======  ======= 
TOTAL                              7.5G     2690 
TOTAL, minus reserved VM space     6.6G     2690"""

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
0x00000028 0x54321654
0x0000002C 0x12341234
0x00000030 0x99999999
0x00000034 0xAAAAAAAA
0x00000038 0xBBBBBBBB
0x0000003C 0xCCCCCCCC
0x00000040 0xDDDDDDDD
0x00000044 0xEEEEEEEE
0x00000048 0xFFFFFFFF
0x0000004C 0x55555555
0x00000050 0x66666666
0x00000054 0x77777777
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
  <EventData>
    <Data>SystemUpdate.exe</Data>
    <Data>1.0.0.0</Data>
    <Data>5a65739b</Data>
    <Data>ntdll.dll</Data>
    <Data>10.0.19041.662</Data>
    <Data>ef4551e9</Data>
    <Data>0xc0000005</Data>
    <Data>00000000000489e8</Data>
    <Data>13f8</Data>
    <Data>01d6bd21c70060b4</Data>
    <Data>C:\Path\To\SystemUpdate.exe</Data>
    <Data>C:\Windows\SYSTEM32\ntdll.dll</Data>
    <Data>0d5e238d-85b7-4b41-9681-1cf64cbe2d4e</Data>
    <Data>
    </Data>
    <Data>
    </Data>
  </EventData>
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
abort() called

Application Specific Backtrace 1:
0   CoreFoundation                      0x00007fff8d8ab03c __exceptionPreprocess + 172
1   libobjc.A.dylib                     0x00007fff8aff676e objc_exception_throw + 43
2   CoreFoundation                      0x00007fff8d8aaeed +[NSException raise:format:] + 205
3   CloudDocsDaemon                     0x00000001069b4d03 __21-[PQLConnection init]_block_invoke_2 + 67
4   CloudDocsDaemon                     0x00000001069b9492 -[PQLConnection _execute:mustSucceed:bindings:] + 650
5   CloudDocsDaemon                     0x00000001069b68f3 -[PQLConnection flush] + 489
6   CloudDocsDaemon                     0x00000001069b7227 -[PQLConnection _performWithFlags:action:whenFlushed:] + 2066
7   CloudDocsDaemon                     0x00000001069b7a40 __41-[PQLConnection performWithFlags:action:]_block_invoke + 36
8   libdispatch.dylib                   0x00007fff8718ac13 _dispatch_client_callout + 8
9   libdispatch.dylib                   0x00007fff8718be5e _dispatch_barrier_sync_f_invoke + 57
10  CloudDocsDaemon                     0x00000001069b7996 -[PQLConnection performWithFlags:action:] + 364
11  CloudDocsDaemon                     0x0000000106936f76 -[BRCAccountSession createPrivateContainerIfNeeded:] + 1159
12  CloudDocsDaemon                     0x0000000106939149 __48-[BRCAccountSession cloudDocsAppsListDidChange:]_block_invoke + 78
13  CoreFoundation                      0x00007fff8d80b1f5 __65-[__NSDictionaryI enumerateKeysAndObjectsWithOptions:usingBlock:]_block_invoke + 85
14  CoreFoundation                      0x00007fff8d80b119 -[__NSDictionaryI enumerateKeysAndObjectsWithOptions:usingBlock:] + 265
15  CloudDocsDaemon                     0x0000000106939068 -[BRCAccountSession cloudDocsAppsListDidChange:] + 271
16  CloudDocsDaemon                     0x000000010698f0b4 -[BRCCloudDocsAppsMonitor addObserver:] + 274
17  CloudDocsDaemon                     0x0000000106934aed -[BRCAccountSession resume] + 404
18  CloudDocsDaemon                     0x00000001068ae4a8 -[BRCDaemon resume] + 108
19  bird                                0x000000010685d7ec bird + 6124
20  libdyld.dylib                       0x00007fff84bb55c9 start + 1

Thread 0 Crashed:: Dispatch queue: com.apple.sqlite.clientTruth
0   libsystem_kernel.dylib        	0x00007fff8a6f5286 __pthread_kill + 10
1   libsystem_c.dylib             	0x00007fff90f82b53 abort + 129
2   libc++abi.dylib               	0x00007fff864c8a21 abort_message + 257
3   libc++abi.dylib               	0x00007fff864f09d1 default_terminate_handler() + 267
4   libobjc.A.dylib               	0x00007fff8affa7d6 _objc_terminate() + 103
5   libc++abi.dylib               	0x00007fff864ee0a1 std::__terminate(void (*)()) + 8
6   libc++abi.dylib               	0x00007fff864ee113 std::terminate() + 51
7   libobjc.A.dylib               	0x00007fff8affa5ff objc_terminate + 9
8   libdispatch.dylib             	0x00007fff8718ac27 _dispatch_client_callout + 28
9   libdispatch.dylib             	0x00007fff8718be5e _dispatch_barrier_sync_f_invoke + 57
10  com.apple.CloudDocsDaemon     	0x00000001069b7996 -[PQLConnection performWithFlags:action:] + 364
11  com.apple.CloudDocsDaemon     	0x0000000106936f76 -[BRCAccountSession createPrivateContainerIfNeeded:] + 1159
12  com.apple.CloudDocsDaemon     	0x0000000106939149 __48-[BRCAccountSession cloudDocsAppsListDidChange:]_block_invoke + 78
13  com.apple.CoreFoundation      	0x00007fff8d80b1f5 __65-[__NSDictionaryI enumerateKeysAndObjectsWithOptions:usingBlock:]_block_invoke + 85
14  com.apple.CoreFoundation      	0x00007fff8d80b119 -[__NSDictionaryI enumerateKeysAndObjectsWithOptions:usingBlock:] + 265
15  com.apple.CloudDocsDaemon     	0x0000000106939068 -[BRCAccountSession cloudDocsAppsListDidChange:] + 271
16  com.apple.CloudDocsDaemon     	0x000000010698f0b4 -[BRCCloudDocsAppsMonitor addObserver:] + 274
17  com.apple.CloudDocsDaemon     	0x0000000106934aed -[BRCAccountSession resume] + 404
18  com.apple.CloudDocsDaemon     	0x00000001068ae4a8 -[BRCDaemon resume] + 108
19  bird                          	0x000000010685d7ec 0x10685c000 + 6124
20  libdyld.dylib                 	0x00007fff84bb55c9 start + 1

Thread 1:: Dispatch queue: com.apple.libdispatch-manager
0   libsystem_kernel.dylib        	0x00007fff8a6f6232 kevent64 + 10
1   libdispatch.dylib             	0x00007fff8718da6a _dispatch_mgr_thread + 52

Thread 2:: Dispatch queue: com.apple.cloudkit.behavioroptions
0   libsystem_kernel.dylib        	0x00007fff8a6f051a semaphore_wait_trap + 10
1   libdispatch.dylib             	0x00007fff87191c55 _dispatch_semaphore_wait_slow + 213
2   com.apple.cloudkit.CloudKit   	0x00007fff85498575 -[CKBehaviorOptions _behaviorOptionForKey:] + 291
3   com.apple.cloudkit.CloudKit   	0x00007fff85498a82 __55-[CKBehaviorOptions _getBoolOptionForKey:defaultValue:]_block_invoke + 148
4   libdispatch.dylib             	0x00007fff8718ac13 _dispatch_client_callout + 8
5   libdispatch.dylib             	0x00007fff8718be5e _dispatch_barrier_sync_f_invoke + 57
6   com.apple.cloudkit.CloudKit   	0x00007fff8549893a -[CKBehaviorOptions _getBoolOptionForKey:defaultValue:] + 227
7   com.apple.cloudkit.CloudKit   	0x00007fff8549cb10 -[CKOperation init] + 416
8   com.apple.cloudkit.CloudKit   	0x00007fff8546c63b -[CKModifyRecordZonesOperation init] + 44
9   com.apple.cloudkit.CloudKit   	0x00007fff8546c72c -[CKModifyRecordZonesOperation initWithRecordZonesToSave:recordZoneIDsToDelete:] + 61
10  com.apple.CloudDocsDaemon     	0x0000000106899cf9 -[_BRCOperation(CKOperationHelpers) addZoneCreationWithZoneID:completion:] + 185
11  com.apple.CloudDocsDaemon     	0x000000010698cf30 -[BRCSyncDownOperation main] + 491
12  com.apple.CloudDocsDaemon     	0x000000010686b614 __dispatch_async_and_inherit_log_sections_block_invoke + 92
13  libdispatch.dylib             	0x00007fff8718f323 _dispatch_call_block_and_release + 12
14  libdispatch.dylib             	0x00007fff8718ac13 _dispatch_client_callout + 8
15  libdispatch.dylib             	0x00007fff8718e365 _dispatch_queue_drain + 1100
16  libdispatch.dylib             	0x00007fff8718fecc _dispatch_queue_invoke + 202
17  libdispatch.dylib             	0x00007fff8718d6b7 _dispatch_root_queue_drain + 463
18  libdispatch.dylib             	0x00007fff8719bfe4 _dispatch_worker_thread3 + 91
19  libsystem_pthread.dylib       	0x00007fff86866637 _pthread_wqthread + 729
20  libsystem_pthread.dylib       	0x00007fff8686440d start_wqthread + 13

Thread 3:
0   libsystem_kernel.dylib        	0x00007fff8a6f594a __workq_kernreturn + 10
1   libsystem_pthread.dylib       	0x00007fff8686440d start_wqthread + 13

Thread 4:: Dispatch queue: com.apple.launchService.exceptionsSerialQueue
0   libsystem_malloc.dylib        	0x00007fff8f2d83ac tiny_free_list_add_ptr + 406
1   libsystem_malloc.dylib        	0x00007fff8f2d553e tiny_malloc_from_free_list + 1450
2   libsystem_malloc.dylib        	0x00007fff8f2d3f50 szone_malloc_should_clear + 317
3   libsystem_malloc.dylib        	0x00007fff8f2d3877 malloc_zone_malloc + 71
4   com.apple.CoreFoundation      	0x00007fff8d749e0e _CFRuntimeCreateInstance + 350
5   com.apple.CoreFoundation      	0x00007fff8d7498e7 CFBasicHashCreate + 135
6   com.apple.CoreFoundation      	0x00007fff8d78e2aa __CFDictionaryCreateTransfer + 138
7   com.apple.CoreFoundation      	0x00007fff8d78df59 __CFBinaryPlistCreateObjectFiltered + 8377
8   com.apple.CoreFoundation      	0x00007fff8d78da78 __CFBinaryPlistCreateObjectFiltered + 7128
9   com.apple.CoreFoundation      	0x00007fff8d78da78 __CFBinaryPlistCreateObjectFiltered + 7128
10  com.apple.CoreFoundation      	0x00007fff8d78da78 __CFBinaryPlistCreateObjectFiltered + 7128
11  com.apple.CoreFoundation      	0x00007fff8d76e057 __CFTryParseBinaryPlist + 215
12  com.apple.CoreFoundation      	0x00007fff8d76d909 _CFPropertyListCreateWithData + 89
13  com.apple.CoreFoundation      	0x00007fff8d79c672 CFPropertyListCreateFromXMLData + 130
14  com.apple.LaunchServices      	0x00007fff8986aaa6 _LSExceptionsLoad + 178
15  com.apple.LaunchServices      	0x00007fff8986a9d3 _LSExceptionsCreate + 134
16  com.apple.LaunchServices      	0x00007fff8986a92a ___LSExceptionsRetainSharedInstance_block_invoke_2 + 36
17  libdispatch.dylib             	0x00007fff8718ac13 _dispatch_client_callout + 8
18  libdispatch.dylib             	0x00007fff8718be5e _dispatch_barrier_sync_f_invoke + 57
19  com.apple.LaunchServices      	0x00007fff8986a8b2 _LSExceptionsRetainSharedInstance + 130
20  com.apple.LaunchServices      	0x00007fff89898a73 _LSAppInfoMeetsMinimumVersionRequirement + 41
21  com.apple.LaunchServices      	0x00007fff898a2509 _LSRegisterDirectoryNode(LSContext*, FSNode*, FSNode*, LSRegistrationInfo*, __CFData const*, __CFDictionary const*, __CFArray**, unsigned char*, unsigned int*) + 1273
22  com.apple.LaunchServices      	0x00007fff898a17db _LSRegisterBundleNode(LSContext*, unsigned int, FSNode*, FSNode*, unsigned int, __CFDictionary const*, __CFArray**, unsigned char*, unsigned int*) + 1070
23  com.apple.LaunchServices      	0x00007fff8986841c _LSFindOrRegisterBundleNode + 1768
24  com.apple.LaunchServices      	0x00007fff8990f335 _LSRegisterNode + 77
25  com.apple.LaunchServices      	0x00007fff898f8907 LSRegisterURL + 89
26  com.apple.CloudDocsDaemon     	0x00000001069290bd BRCRegisterPackageExtension + 997
27  com.apple.CloudDocsDaemon     	0x000000010693371a -[BRCAccountSession registerPackageExtension:] + 59
28  com.apple.CloudDocsDaemon     	0x0000000106933657 -[BRCAccountSession _setupSharedPackageExtensionsApp] + 714
29  libdispatch.dylib             	0x00007fff8718f323 _dispatch_call_block_and_release + 12
30  libdispatch.dylib             	0x00007fff8718ac13 _dispatch_client_callout + 8
31  libdispatch.dylib             	0x00007fff8718e365 _dispatch_queue_drain + 1100
32  libdispatch.dylib             	0x00007fff8718fecc _dispatch_queue_invoke + 202
33  libdispatch.dylib             	0x00007fff8718d6b7 _dispatch_root_queue_drain + 463
34  libdispatch.dylib             	0x00007fff8719bfe4 _dispatch_worker_thread3 + 91
35  libsystem_pthread.dylib       	0x00007fff86866637 _pthread_wqthread + 729
36  libsystem_pthread.dylib       	0x00007fff8686440d start_wqthread + 13

Thread 5:: Dispatch queue: sync/sharedb
0   libsystem_kernel.dylib        	0x00007fff8a6f051a semaphore_wait_trap + 10
1   libsystem_platform.dylib      	0x00007fff8e9bfc5b _os_semaphore_wait + 16
2   libdispatch.dylib             	0x00007fff87194557 _dispatch_barrier_sync_f_slow + 597
3   com.apple.cloudkit.CloudKit   	0x00007fff8549893a -[CKBehaviorOptions _getBoolOptionForKey:defaultValue:] + 227
4   com.apple.cloudkit.CloudKit   	0x00007fff8549cb10 -[CKOperation init] + 416
5   com.apple.cloudkit.CloudKit   	0x00007fff854ba1bc -[CKModifySubscriptionsOperation initWithSubscriptionsToSave:subscriptionIDsToDelete:] + 79
6   com.apple.CloudDocsDaemon     	0x000000010686c01d -[BRCSharedDatabaseSyncOperation _performAfterRegisteringForPushes:] + 170
7   com.apple.CloudDocsDaemon     	0x000000010686d557 -[BRCSharedDatabaseSyncOperation main] + 233
8   com.apple.CloudDocsDaemon     	0x000000010686b614 __dispatch_async_and_inherit_log_sections_block_invoke + 92
9   libdispatch.dylib             	0x00007fff8718f323 _dispatch_call_block_and_release + 12
10  libdispatch.dylib             	0x00007fff8718ac13 _dispatch_client_callout + 8
11  libdispatch.dylib             	0x00007fff8718e365 _dispatch_queue_drain + 1100
12  libdispatch.dylib             	0x00007fff8718fecc _dispatch_queue_invoke + 202
13  libdispatch.dylib             	0x00007fff8718d6b7 _dispatch_root_queue_drain + 463
14  libdispatch.dylib             	0x00007fff8719bfe4 _dispatch_worker_thread3 + 91
15  libsystem_pthread.dylib       	0x00007fff86866637 _pthread_wqthread + 729
16  libsystem_pthread.dylib       	0x00007fff8686440d start_wqthread + 13

Thread 0 crashed with X86 Thread State (64-bit):
  rax: 0x0000000000000000  rbx: 0x0000000000000006  rcx: 0x00007fff593a30e8  rdx: 0x0000000000000000
  rdi: 0x000000000000140f  rsi: 0x0000000000000006  rbp: 0x00007fff593a3110  rsp: 0x00007fff593a30e8
   r8: 0x6e6f697470656378   r9: 0x00007fff90facd70  r10: 0x0000000008000000  r11: 0x0000000000000206
  r12: 0x00007fff593a3270  r13: 0x00007fc8d0427220  r14: 0x00007fff74107300  r15: 0x00007fff593a3150
  rip: 0x00007fff8a6f5286  rfl: 0x0000000000000206  cr2: 0x00007fff758c2fd8
  
Logical CPU:     0
Error Code:      0x02000148
Trap Number:     133


Binary Images:
       0x10685c000 -        0x10685dfff  bird (321.6) <16D08E4D-FB56-3839-B03F-36F6BC78DCD7> /System/Library/PrivateFrameworks/CloudDocsDaemon.framework/Versions/A/Support/bird
       0x106866000 -        0x106a3ffff  com.apple.CloudDocsDaemon (1.0 - 321.6) <AF26C608-8AEA-3210-A187-A019ECC68F38> /System/Library/PrivateFrameworks/CloudDocsDaemon.framework/Versions/A/CloudDocsDaemon
       0x106b5b000 -        0x106b62fff  com.apple.CacheDelete (1.0 - 1) <B1800E38-6208-3E66-8D48-7A7A2F085EB0> /System/Library/PrivateFrameworks/CacheDelete.framework/Versions/A/CacheDelete
       0x106b9a000 -        0x106ba9fff  libSimplifiedChineseConverter.dylib (64) <468DE6E1-42B9-3751-ACA5-7D16C550FF84> /System/Library/CoreServices/Encodings/libSimplifiedChineseConverter.dylib
    0x7fff609be000 -     0x7fff609f4837  dyld (353.2.1) <65DCCB06-339C-3E25-9702-600A28291D0E> /usr/lib/dyld
    0x7fff8372c000 -     0x7fff83746ff3  com.apple.Ubiquity (1.3 - 313) <DF56A657-CC6E-3BE2-86A0-71F07127724C> /System/Library/PrivateFrameworks/Ubiquity.framework/Versions/A/Ubiquity
    0x7fff83747000 -     0x7fff8383bfff  libFontParser.dylib (134.2) <9F57B025-AB9C-31DD-9D54-2D7AB1298885> /System/Library/Frameworks/ApplicationServices.framework/Versions/A/Frameworks/ATS.framework/Versions/A/Resources/libFontParser.dylib
    0x7fff83bd5000 -     0x7fff83bddfff  libMatch.1.dylib (24) <C917279D-33C2-38A8-9BDD-18F3B24E6FBD> /usr/lib/libMatch.1.dylib
    0x7fff83bde000 -     0x7fff83c29fff  com.apple.CloudDocs (1.0 - 321.6) <4C54EDB7-4377-3722-8C47-F3C3D260FCBA> /System/Library/PrivateFrameworks/CloudDocs.framework/Versions/A/CloudDocs
    0x7fff83c2a000 -     0x7fff83c44ff7  liblzma.5.dylib (7) <1D03E875-A7C0-3028-814C-3C27F7B7C079> /usr/lib/liblzma.5.dylib
    0x7fff85135000 -     0x7fff85183fff  libcurl.4.dylib (83.1.2) <462767FC-C7F2-39F1-8C10-DA4114945F55> /usr/lib/libcurl.4.dylib
    0x7fff85184000 -     0x7fff8519dff7  com.apple.CFOpenDirectory (10.10 - 187) <790ED527-EFD2-3EA6-8C97-A8C04E96EBA7> /System/Library/Frameworks/OpenDirectory.framework/Versions/A/Frameworks/CFOpenDirectory.framework/Versions/A/CFOpenDirectory
    0x7fff8519e000 -     0x7fff851aaff7  com.apple.commonutilities (8.0 - 900) <E5E018A7-FB3C-37A2-9769-49AFAC89FDE8> /System/Library/PrivateFrameworks/CommonUtilities.framework/Versions/A/CommonUtilities
    0x7fff851ab000 -     0x7fff851b3ff7  com.apple.AppleSRP (5.0 - 1) <01EC5144-D09A-3D6A-AE35-F6D48585F154> /System/Library/PrivateFrameworks/AppleSRP.framework/Versions/A/AppleSRP
    0x7fff851b4000 -     0x7fff851b6fff  libRadiance.dylib (1237) <9B048776-53BB-3947-8ECE-9DDA804C86B2> /System/Library/Frameworks/ImageIO.framework/Versions/A/Resources/libRadiance.dylib
    0x7fff8525c000 -     0x7fff852bbfff  com.apple.AE (681.2 - 681.2) <181B3B06-2DC6-3E4D-B44A-2551C5E9CF6F> /System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/AE.framework/Versions/A/AE
    0x7fff852d2000 -     0x7fff852d2fff  com.apple.quartzframework (1.5 - 1.5) <26C982A3-2FC3-3F50-B5F4-3C545C3BAC10> /System/Library/Frameworks/Quartz.framework/Versions/A/Quartz
    0x7fff852d3000 -     0x7fff852edff7  libextension.dylib (55.2) <3BB019CA-199A-36AC-AA22-14B562138545> /usr/lib/libextension.dylib
    0x7fff852ee000 -     0x7fff85360fff  com.apple.framework.IOKit (2.0.2 - 1050.20.2) <09C0518C-90DF-3FC3-96D6-34D35F72C8EF> /System/Library/Frameworks/IOKit.framework/Versions/A/IOKit
    0x7fff85361000 -     0x7fff85364ff7  com.apple.AppleSystemInfo (3.1.5 - 3.1.5) <BCC15965-7869-34F4-9019-9D0A41DD6AFF> /System/Library/PrivateFrameworks/AppleSystemInfo.framework/Versions/A/AppleSystemInfo
    0x7fff85466000 -     0x7fff854fcff7  com.apple.cloudkit.CloudKit (283.67.2 - 283.67.2) <79F5AD38-61D5-30E6-96DC-974351D4195B> /System/Library/Frameworks/CloudKit.framework/Versions/A/CloudKit
    0x7fff8550a000 -     0x7fff8551cff7  libsasl2.2.dylib (194.1) <35371406-75EF-304A-A073-956C40373555> /usr/lib/libsasl2.2.dylib
    0x7fff8551d000 -     0x7fff85a0dfff  com.apple.MediaToolbox (1.0 - 1562.235) <9813E9A6-5BD6-3E56-9D20-0023703D5096> /System/Library/Frameworks/MediaToolbox.framework/Versions/A/MediaToolbox
    0x7fff85afb000 -     0x7fff85b60ff7  com.apple.ids (10.0 - 1000) <42C61956-F016-315A-ADD3-3CA37EE99DD7> /System/Library/PrivateFrameworks/IDS.framework/Versions/A/IDS
    0x7fff85d33000 -     0x7fff85d6affb  com.apple.LDAPFramework (2.4.28 - 194.5) <CAFB9695-000F-34EA-8DF5-09996929C26A> /System/Library/Frameworks/LDAP.framework/Versions/A/LDAP
    0x7fff85fca000 -     0x7fff861d7ff3  com.apple.CFNetwork (720.3.13 - 720.3.13) <69E15385-5784-3912-88F6-03B16F1C1A5C> /System/Library/Frameworks/CFNetwork.framework/Versions/A/CFNetwork
    0x7fff861d8000 -     0x7fff86276fff  com.apple.Metadata (10.7.0 - 917.35) <8CBD1D32-4F4B-3F9A-AC65-76F2B5376FBF> /System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/Metadata.framework/Versions/A/Metadata
    0x7fff86277000 -     0x7fff86332ff7  com.apple.DiscRecording (9.0 - 9000.4.2) <4655B4B8-523D-3AE6-92A0-8486A2258B3B> /System/Library/Frameworks/DiscRecording.framework/Versions/A/DiscRecording
    0x7fff86333000 -     0x7fff86334ff7  libsystem_blocks.dylib (65) <9615D10A-FCA7-3BE4-AA1A-1B195DACE1A1> /usr/lib/system/libsystem_blocks.dylib
    0x7fff86335000 -     0x7fff8633aff7  com.apple.MediaAccessibility (1.0 - 61) <00A3E0B6-79AC-387E-B282-AADFBD5722F6> /System/Library/Frameworks/MediaAccessibility.framework/Versions/A/MediaAccessibility
    0x7fff8633b000 -     0x7fff8633cff7  com.apple.AddressBook.ContactsData (9.0 - 1579) <FF9C31DD-7839-35FB-AE66-21AEF63583EF> /System/Library/PrivateFrameworks/ContactsData.framework/Versions/A/ContactsData
    0x7fff8633d000 -     0x7fff8633efff  com.apple.TrustEvaluationAgent (2.0 - 25) <2D61A2C3-C83E-3A3F-8EC1-736DBEC250AB> /System/Library/PrivateFrameworks/TrustEvaluationAgent.framework/Versions/A/TrustEvaluationAgent
    0x7fff8633f000 -     0x7fff86360fff  com.apple.framework.Apple80211 (10.3 - 1030.71.6) <D3862426-2586-3DF7-BA75-9A184FCD74C4> /System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Apple80211
    0x7fff864c8000 -     0x7fff864f3fff  libc++abi.dylib (125) <88A22A0F-87C6-3002-BFBA-AC0F2808B8B9> /usr/lib/libc++abi.dylib
    0x7fff864f4000 -     0x7fff864ffff7  com.apple.speech.synthesis.framework (5.3.3 - 5.3.3) <A5640275-E2A6-3856-95EF-5F0DC440B10C> /System/Library/Frameworks/ApplicationServices.framework/Versions/A/Frameworks/SpeechSynthesis.framework/Versions/A/SpeechSynthesis
    0x7fff86500000 -     0x7fff86628ff7  com.apple.coreui (2.1 - 308.6) <DEA5D3E1-D333-302B-A6CF-7643BFDFAED0> /System/Library/PrivateFrameworks/CoreUI.framework/Versions/A/CoreUI
    0x7fff86629000 -     0x7fff8668efff  com.apple.framework.internetaccounts (2.1 - 210) <7CAE7A16-0422-3817-B3AB-478F756768F4> /System/Library/PrivateFrameworks/InternetAccounts.framework/Versions/A/InternetAccounts
    0x7fff86729000 -     0x7fff8672cfff  com.apple.xpc.ServiceManagement (1.0 - 1) <9E025823-660A-30C5-A568-223BD595B6F7> /System/Library/Frameworks/ServiceManagement.framework/Versions/A/ServiceManagement
    0x7fff86779000 -     0x7fff8677affb  libremovefile.dylib (35) <3485B5F4-6CE8-3C62-8DFD-8736ED6E8531> /usr/lib/system/libremovefile.dylib
    0x7fff8677b000 -     0x7fff867e2ff7  com.apple.framework.CoreWiFi (3.0 - 300.4) <19269C1D-EB29-384A-83F3-7DDDEB7D9DAD> /System/Library/PrivateFrameworks/CoreWiFi.framework/Versions/A/CoreWiFi
    0x7fff867e3000 -     0x7fff867eeff7  com.apple.CrashReporterSupport (10.10 - 631) <D87A64FA-64B1-3B23-BB43-ADE173C108C6> /System/Library/PrivateFrameworks/CrashReporterSupport.framework/Versions/A/CrashReporterSupport
    0x7fff867ef000 -     0x7fff86815fff  com.apple.ChunkingLibrary (2.1 - 163.6) <29D4CB95-42EF-34C6-8182-BDB6F7BB1E79> /System/Library/PrivateFrameworks/ChunkingLibrary.framework/Versions/A/ChunkingLibrary
    0x7fff86863000 -     0x7fff8686cfff  libsystem_pthread.dylib (105.10.1) <3103AA7F-3BAE-3673-9649-47FFD7E15C97> /usr/lib/system/libsystem_pthread.dylib
    0x7fff8686d000 -     0x7fff86914fff  com.apple.PDFKit (3.1 - 3.1) <717B6DB9-4C81-3326-AFB7-6B003FBF1311> /System/Library/Frameworks/Quartz.framework/Versions/A/Frameworks/PDFKit.framework/Versions/A/PDFKit
    0x7fff86915000 -     0x7fff86afaff7  libicucore.A.dylib (531.48) <3CD34752-B1F9-31D2-865D-B5B0F0BE3111> /usr/lib/libicucore.A.dylib
    0x7fff86ba7000 -     0x7fff86bc7fff  com.apple.IconServices (47.1 - 47.1) <E83DFE3B-6541-3736-96BB-26DC5D0100F1> /System/Library/PrivateFrameworks/IconServices.framework/Versions/A/IconServices
    0x7fff86bf1000 -     0x7fff86c1eff7  com.apple.Accounts (113 - 113) <17D8868C-7079-354F-8F37-B8346960D94B> /System/Library/Frameworks/Accounts.framework/Versions/A/Accounts
    0x7fff86c26000 -     0x7fff86c26fff  com.apple.ApplicationServices (48 - 48) <5BF7910B-C328-3BF8-BA4F-CE52B574CE01> /System/Library/Frameworks/ApplicationServices.framework/Versions/A/ApplicationServices
    0x7fff86de8000 -     0x7fff86e2eff7  libFontRegistry.dylib (134.1) <CE41D8C2-BEED-345C-BC4F-3775CC06C672> /System/Library/Frameworks/ApplicationServices.framework/Versions/A/Frameworks/ATS.framework/Versions/A/Resources/libFontRegistry.dylib
    0x7fff87052000 -     0x7fff870e0ff7  com.apple.CorePDF (4.0 - 4) <9CD7EC6D-3593-3D60-B04F-75F612CCB99A> /System/Library/PrivateFrameworks/CorePDF.framework/Versions/A/CorePDF
    0x7fff870e1000 -     0x7fff87178fff  com.apple.CoreMedia (1.0 - 1562.235) <21EB4AB6-2DBC-326B-B17E-E88BAA9E9200> /System/Library/Frameworks/CoreMedia.framework/Versions/A/CoreMedia
    0x7fff87179000 -     0x7fff87188fff  com.apple.LangAnalysis (1.7.0 - 1.7.0) <D1E527E4-C561-352F-9457-E8C50232793C> /System/Library/Frameworks/ApplicationServices.framework/Versions/A/Frameworks/LangAnalysis.framework/Versions/A/LangAnalysis
    0x7fff87189000 -     0x7fff871b3ff7  libdispatch.dylib (442.1.4) <502CF32B-669B-3709-8862-08188225E4F0> /usr/lib/system/libdispatch.dylib
    0x7fff871b4000 -     0x7fff871b4ff7  liblaunch.dylib (559.20.9) <FA89A113-696E-3271-8FE1-A0D7324E8481> /usr/lib/system/liblaunch.dylib
    0x7fff871b5000 -     0x7fff87221fff  com.apple.framework.CoreWLAN (5.0 - 500.35.2) <5E228544-77A9-3AA5-8355-E8F6626F50E7> /System/Library/Frameworks/CoreWLAN.framework/Versions/A/CoreWLAN
    0x7fff8999b000 -     0x7fff89eb0ffb  com.apple.JavaScriptCore (10600 - 10600.5.10) <ED4CABC6-0952-3E28-A3CD-32CA5CE22252> /System/Library/Frameworks/JavaScriptCore.framework/Versions/A/JavaScriptCore
    0x7fff89eb1000 -     0x7fff89f87ff3  com.apple.DiskImagesFramework (10.10.1 - 396) <1149D3E1-CC6C-3177-916D-2BE066DC9344> /System/Library/PrivateFrameworks/DiskImages.framework/Versions/A/DiskImages
    0x7fff89f88000 -     0x7fff8a138ff3  com.apple.QuartzCore (1.10 - 361.18) <ACA61D8F-9535-3141-8FDD-AC3EF6BF0806> /System/Library/Frameworks/QuartzCore.framework/Versions/A/QuartzCore
    0x7fff8a139000 -     0x7fff8a140fff  com.apple.network.statistics.framework (1.2 - 1) <61B311D1-7F15-35B3-80D4-99B8BE90ACD9> /System/Library/PrivateFrameworks/NetworkStatistics.framework/Versions/A/NetworkStatistics
    0x7fff8a141000 -     0x7fff8a143fff  libquarantine.dylib (76.20.1) <7AF90041-2768-378A-925A-D83161863642> /usr/lib/system/libquarantine.dylib
    0x7fff8a144000 -     0x7fff8a174fff  libsystem_m.dylib (3086.1) <1E12AB45-6D96-36D0-A226-F24D9FB0D9D6> /usr/lib/system/libsystem_m.dylib
    0x7fff8a175000 -     0x7fff8a182ff7  com.apple.SpeechRecognitionCore (2.1.2 - 2.1.2) <551322E2-C1E4-3378-A218-F362985E3E3C> /System/Library/PrivateFrameworks/SpeechRecognitionCore.framework/Versions/A/SpeechRecognitionCore
    0x7fff8a1ad000 -     0x7fff8a214ffb  com.apple.datadetectorscore (6.0 - 396.1.1) <9B0B3198-DDBE-36C0-8BA9-3EC89C725282> /System/Library/PrivateFrameworks/DataDetectorsCore.framework/Versions/A/DataDetectorsCore
    0x7fff8a215000 -     0x7fff8a283ffb  com.apple.Heimdal (4.0 - 2.0) <7697A837-98B8-3BDB-A7D2-8ED4C9ABC510> /System/Library/PrivateFrameworks/Heimdal.framework/Versions/A/Heimdal"""

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
generate_crash_report(is_long, is_silly)

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
