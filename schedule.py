import time
def calcTime(ti):

    # total seconds to be waited
    result = 0

    # current time
    ct = time.localtime()

    # current hour
    ct_hour = int(time.strftime("%H", ct))

    #current minute
    ct_minute = int(time.strftime("%M", ct))

    # targeted hour
    ti_hour = int(ti[0:ti.index(':')])

    # targeted minute
    ti_minute = int(ti[ti.index(':')+1:])

    # minutes to be waited
    m_result = ti_minute - ct_minute

    # in case the targeted minute is less than the current minute 
    if (m_result < 0):
        m_result += 60
        ti_hour -= 1
        if (ti_hour < 0):
            ti_hour = 23

    # calculates the minutes to be waited into seconds
    result += 60*m_result

    # hours to be waited
    h_result = ti_hour - ct_hour

    # in case the targeted hour is less than the current hour 
    if (h_result < 0):
        h_result += 24

    # calculates the hours to be waited into seconds
    result += 60 * 60 * h_result

    # reutrns the total seconds to be waited
    return result

# sleeps the application until the time input arrives
def timer(timeInput):
    time.sleep(calcTime(timeInput))
