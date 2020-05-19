from hoshino import Service
from .calendar import *

svjp = Service('calendar-jp', enable_on_default=False)
svbl = Service('calendar-bili', enable_on_default=False)


@svjp.scheduled_job('cron', minute='08', jitter=20)
async def jp_check_ver():
    check_ver(svjp, 'jp')


@svbl.scheduled_job('cron', minute='02', jitter=20)
async def bl_check_ver():
    check_ver(svbl, 'bili')


@svjp.scheduled_job('cron', hour='15', minute='05')
async def push_jp_calendar():
    await svjp.broadcast(db_message(svjp, 'jp'), 'calendar-jp')


@svbl.scheduled_job('cron', hour='15', minute='15')
async def push_bl_calendar():
    await svbl.broadcast(db_message(svbl, 'bili'), 'calendar-bilibili')


@svjp.on_rex(r'^日服(当前|预定)?日程$', normalize=True, event='group')
async def look_jp_calendar(bot, ctx, match):
    is_now = match.group(1) == '当前'
    is_future = match.group(1) == '预定'
    is_all = not match.group(1)
    if is_now:
        await bot.send(ctx, db_message(svjp, 'jp', 'now'), at_sender=True)
    if is_future:
        await bot.send(ctx, db_message(svjp, 'jp', 'future'), at_sender=True)
    if is_all:
        await bot.send(ctx, db_message(svjp, 'jp', 'all'), at_sender=True)


@svbl.on_rex(r'^[bB国]服(当前|预定)?日程$', normalize=True, event='group')
async def look_bilibili_calendar(bot, ctx, match):
    is_now = match.group(1) == '当前'
    is_future = match.group(1) == '预定'
    is_all = not match.group(1)
    if is_now:
        await bot.send(ctx, db_message(svbl, 'bili', 'now'), at_sender=True)
    if is_future:
        await bot.send(ctx, db_message(svbl, 'bili', 'future'), at_sender=True)
    if is_all:
        await bot.send(ctx, db_message(svbl, 'bili', 'all'), at_sender=True)
