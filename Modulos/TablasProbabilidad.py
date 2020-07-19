from Modulos.Constantes import DecisionMontecarlo

def CrearProbabilidadesAcumuladas(prob):
    v = [0] * (len(prob) + 1)
    for i in range(len(prob)):
        v[i + 1] = v[i] + prob[i]
    return v

def CrearIntervalos(prob):
    prob_acumuladas = CrearProbabilidadesAcumuladas(prob)
    intervalos = []
    for i in range(len(prob_acumuladas) - 1):
        intervalos.append(str(prob_acumuladas[i]) + " - " + str(prob_acumuladas[i + 1]))
    return intervalos

def CalcularDecisionCliente(prob, nro_aleatorio):
    len_lista = len(prob)
    nro_aleatorio = nro_aleatorio * 100
    indice = 0
    for i in range(len_lista - 1):
        if i == len_lista - 2:
            if prob[i] <= nro_aleatorio <= prob[i + 1]:
                indice = i
                break
        if prob[i] <= nro_aleatorio < prob[i + 1]:
            indice = i
            break
    if indice == 2:
        return DecisionMontecarlo.DE_PASO
    elif indice == 1:
        return DecisionMontecarlo.MESA
    elif indice == 0:
        return DecisionMontecarlo.COMPRA
    else:
        raise Exception("El vector de probabilidades acumuladas no se corresponde con los parametros necesarios para la simulacion")