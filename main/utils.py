from datetime import datetime

CATEGORIES = [
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9'
]

def get_category_of_the_day(): 
    
    start_date = datetime(2025, 5, 13).date()
    today = datetime.now().date()

    days_passed = (today - start_date).days
    
    category_index = days_passed % len(CATEGORIES)
    
    return CATEGORIES[category_index]