def print_args_kwargs(arg1,arg2,seconda_chiave, prima_chiave,terza_chiave):
    print terza_chiave
    print arg1
    print arg2
    print seconda_chiave
    print prima_chiave

def print_kwargs(costante_passata,**kwargs):
    print "la costante passata e' %d" % costante_passata
    for key in kwargs:
        print "La chiave: %s il valore %s" % (key, kwargs[key])

posizioni = [12,45]
costante = 10000
chiavi = {'prima_chiave':100, 'seconda_chiave':200, 'terza_chiave':300}
print_args_kwargs(*posizioni, **chiavi)
print_kwargs(costante,**chiavi)

