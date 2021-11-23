# 調整json格式--------------------------------------------------------------------------------
def wrapResult(resault):
    target = "{'data':["
    for doc in resault:
        target += str(doc) + ','
    target = target[:-1] + "]}"
    print(target)
    return target