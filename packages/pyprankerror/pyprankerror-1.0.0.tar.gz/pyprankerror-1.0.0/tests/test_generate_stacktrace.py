import pytest
import sys
import os

# test_generate_stacktrace.py
from src.pyprankerror import generate_stacktrace, short, long, shortfunny, longfunny  # Import the function you want to test
@pytest.fixture


def test_generate_stacktrace_short(capsys):
    generate_stacktrace(length=0, is_silly=False)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Traceback (most recent call last):\n  File \"\\Users\\pyperror\\utils\\migration_utils.py\", line 887, in <module>\n    is_approved = calculate_triangle_area(user_responses)\n  File \"\\Users\\pyperror\\api\\product_api.py\", line 487, in calculate_triangle_area\n    is_approved = validate_user_age(word_count)\n  File \"\\Users\\pyperror\\config\\email_config.py\", line 630, in validate_user_age\n    credit_card_number = validate_product_code(order_status)\nTypeError: unsupported operand type(s) for +: 'int' and 'str'"
    

def test_generate_stacktrace_long(capsys):
    generate_stacktrace(length=1, is_silly=False)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Traceback (most recent call last):\n  File \"\\Users\\pyperror\\models\\category_model.py\", line 998, in <module>\n    reviewer_name = validate_user_age(is_verified)\n  File \"\\Users\\pyperror\\config\\api_config.py\", line 13, in validate_user_age\n    product_rating = validate_phone_number(survey_results)\n  File \"\\Users\\pyperror\\scripts\\data_processing.py\", line 518, in validate_phone_number\n    workshop_duration = process_data(first_name)\n  File \"\\Users\\pyperror\\config\\migration_config.py\", line 536, in process_data\n    attendee_name = generate_transaction_id(workshop_name)\n  File \"\\Users\\pyperror\\utils\\security_utils.py\", line 167, in generate_transaction_id\n    page_count = format_currency(manufacturing_date)\n  File \"\\Users\\pyperror\\utils\\validation_utils.py\", line 176, in format_currency\n    is_in_stock = generate_signature(product_rating)\n  File \"\\Users\\pyperror\\tests\\test_security.py\", line 370, in generate_signature\n    conference_name = send_push_notification(publication_date)\n  File \"\\Users\\pyperror\\tests\\test_api.py\", line 60, in send_push_notification\n    email_address = fetch_data_from_api(product_name)\n  File \"\\Users\\pyperror\\api\\invoice_api.py\", line 850, in fetch_data_from_api\n    event_capacity = check_user_permissions(is_deleted)\n  File \"\\Users\\pyperror\\views\\invoice_view.py\", line 562, in check_user_permissions\n    workshop_name = parse_config_file(response_value)\n  File \"\\Users\\pyperror\\tests\\test_user_management.py\", line 478, in parse_config_file\n    quantity = generate_api_key(price)\n  File \"\\Users\\pyperror\\config\\api_config.py\", line 916, in generate_api_key\n    event_location = parse_binary_data(ticket_price)\n  File \"\\Users\\pyperror\\views\\notification_view.py\", line 103, in parse_binary_data\n    workshop_duration = parse_sensor_signals(publication_date)\nNameError: name 'response_text' is not defined"       
    
def test_generate_stacktrace_shortfunny(capsys):
    generate_stacktrace(length=0, is_silly=True)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Traceback (most recent call last):\n  File \"\\Users\\pyperror\\utils\\string_operations.py\", line 709, in <module>\n    chocolate_rain = predictFuture(starbucks_coffee)\n  File \"\\Users\\pyperror\\tests\\test_models.py\", line 716, in predictFuture\n    gummybearxd = countSheepUntilSleep(lasagna_layers)\n  File \"\\Users\\pyperror\\api\\authentication_api.py\", line 213, in countSheepUntilSleep\n    michael_jackson = confuseCats(jellybeans)\nAttributeError: 'list' object has no attribute 'appendx'"
    
def test_generate_stacktrace_longfunny(capsys):
    generate_stacktrace(length=1, is_silly=True)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Traceback (most recent call last):\n  File \"\\Users\\pyperror\\views\\invoice_view.py\", line 58, in <module>\n    elonmusk = transformIntoAPumpkin(michael_jackson)\n  File \"\\Users\\pyperror\\scripts\\report_generation.py\", line 495, in transformIntoAPumpkin\n    bananas = findMeaningOfLife(joe_biden)\n  File \"\\Users\\pyperror\\config\\config_parser.py\", line 393, in findMeaningOfLife\n    unicorn_num = countSheepUntilSleep(michael_jackson)\n  File \"\\Users\\pyperror\\utils\\migration_utils.py\", line 365, in countSheepUntilSleep\n    gummybearxd = transformIntoAPumpkin(jellybeans)\n  File \"\\Users\\pyperror\\utils\\email_utils.py\", line 657, in transformIntoAPumpkin\n    chocolate_rain = speakInDolphin(lasagna_layers)\n  File \"\\Users\\pyperror\\scripts\\data_migration.py\", line 962, in speakInDolphin\n    spiderman_weblength = brewMagicPotion(minecraft)\n  File \"\\Users\\pyperror\\tests\\test_security.py\", line 923, in brewMagicPotion\n    starbucks_coffee = danceLikeNoOneIsWatching(lasagna_layers)\n  File \"\\Users\\pyperror\\controllers\\supplier_controller.py\", line 735, in danceLikeNoOneIsWatching\n    toiletPaper_Length = createUniverse(bobby_shmurda)\n  File \"\\Users\\pyperror\\views\\profile_view.py\", line 780, in createUniverse\n    toiletPaper_Length = teleportToMars(starbucks_coffee)\n  File \"\\Users\\pyperror\\scripts\\data_processing.py\", line 670, in teleportToMars\n    joe_biden = confuseCats(jellybeans)\n  File \"\\Users\\pyperror\\tests\\test_utils.py\", line 828, in confuseCats\n    jellybeans = predictFuture(starbucks_coffee)\n  File \"\\Users\\pyperror\\tests\\test_import.py\", line 896, in predictFuture\n    michael_jackson = predictFuture(chocolate_rain)\nKeyError: 'option3'"
