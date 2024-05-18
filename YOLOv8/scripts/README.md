Estos son los scripts para realizar las inferencias.
Para probar un modelo con una imagen en un notebook ejecute en una celda:
`$ !yolo task=detect mode=predict model="path/modelo.pt" conf=0.25 source='imagen.jpg' save=True`