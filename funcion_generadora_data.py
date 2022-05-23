class generacion_data_replica_n:
    def __init__(self, recs, nodo, warmtime, trial):
        self.recs = recs
        self.warmtime = warmtime
        self.nodo = nodo
        self.trial = trial

    def obtener_service_time_nodo(self):
        service_time_nodo = [s.service_time for s in self.recs if s.node ==
                             self.nodo if s.arrival_date > self.warmtime]
        #print(f"Retornando lista de tiempos de servicio del nodo {self.nodo} de replica {self.trial}")
        return service_time_nodo

    def obtener_tiempos_en_cola_nodo(self):
        tiempos_espera_nodo = [
            s.waiting_time for s in self.recs if s.node == self.nodo if s.arrival_date > self.warmtime]
        #print(f"Retornando lista de tiempos en cola del nodo{self.nodo} de replica {self.trial}")
        return tiempos_espera_nodo

    def largo_cola_nodo(self):
        largo_cola_nodo = [s.queue_size_at_arrival for s in self.recs if s.node ==
                           self.nodo if s.arrival_date > self.warmtime]
        #print(f"Retornando largo promedio de cola del nodo{self.nodo} de replica {self.trial}")

        return largo_cola_nodo

    def guardar_datos_replica(self, lista_datos_replica, lista_guadar_datos):
        for i in lista_datos_replica:
            lista_guadar_datos.append(i)
        #print(f"Data guardada")
