def filter_func(results, config):
    final = []
    for result in results:
        if result != "filterme":
            final.append(result)
    return final