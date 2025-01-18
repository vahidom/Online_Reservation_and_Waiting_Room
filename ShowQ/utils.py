from datetime import datetime, timedelta, time

def generate_available_times(schedule):
    available_times = {}
    current_date = schedule.start_date

    while current_date <= schedule.end_date:
        times = []
        current_time = datetime.combine(current_date, schedule.start_time)

        end_datetime = datetime.combine(current_date, schedule.end_time)
        while current_time + timedelta(minutes=schedule.appointment_length) <= end_datetime:
            times.append(current_time)
            current_time += timedelta(minutes=schedule.appointment_length)

        available_times[current_date] = times
        current_date += timedelta(days=1)

    return available_times
