import cv2 as cv

class FrameEdge:
    def __init__(self, cap):
        self.cap = cap
        self.frame = None
        self.edge = None
        self.application = None
        self.threshold = [80, 80]
        self.area = [500, 1250]
        self.face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

    def set_threshold(self, lower, upper):
        if lower <= upper:
            if(lower >= 0): self.threshold[0] = lower
            if(upper >= 0): self.threshold[1] = upper

    def set_area(self, lower, upper):
        if lower <= upper:
            if(lower >= 0): self.area[0] = lower
            if(upper >= 0): self.area[1] = upper

    def shader(self):
        flag, self.frame = self.cap.read() # Lê um quadro de captura de vídeo.
        if not flag:
            print("Frame error")
            return False
        self.frame = cv.flip(self.frame, 1) # Inverte horizontalmente a imagem.
        gray = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY) # Converte a imagem de BGR para escala de cinza.

        # No contexto de detecção de bordas, como no caso da função cv.Canny(), o algoritmo analisa as mudanças 
        # na intensidade dos pixels adjacentes. Uma borda é identificada onde há uma transição abrupta na intensidade.
        self.edge = cv.Canny(gray, self.threshold[0], self.threshold[1]) # Detecta bordas em uma imagem.
        self.application = self.frame
        return True
    
    def render_frame(self):
        self.shader()
        cv.imshow('FRAME', self.frame) # Exibe a imagem uma janela.

    def render_edge(self):
        self.shader()
        # text = f'Thresholds: {self.threshold[0]}, {self.threshold[1]}'
        # cv.putText(self.edge, text, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv.LINE_AA)
        cv.imshow('FRAME', self.edge) # Exibe a imagem uma janela.

    def render_contour(self):
        self.shader()
        contours, _ = cv.findContours(self.edge, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE) # Encontra todos os contornos na imagem.
        cv.drawContours(self.application, contours, -1, (255, 0, 0), 1) # Desenha todos os contornos na imagem.
        cv.imshow('FRAME', self.application) # Exibe a imagem em uma janela.
    
    def render_square(self):
        self.shader()
        contours, _ = cv.findContours(self.edge, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE) # Encontra todos os contornos na imagem.
        for cnt in contours:
            area = cv.contourArea(cnt) # Calcula a área do contorno.
            if self.area[0] <= area <= self.area[1]:
                x, y, w, h = cv.boundingRect(cnt) # Obtem o retângulo delimitador para o contorno.
                cv.rectangle(self.application, (x, y), (x + w, y + h), (0, 255, 0), 1) # Desenha um retângulo verde na imagem.
                cv.putText(self.application, f'Area: {int(area)}', (x, y - 5), cv.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1, cv.LINE_AA) # Adiciona um texto acima do retângulo.
        cv.imshow('FRAME', self.application) # Exibe a imagem em uma janela.

    def render_face(self):
        self.shader()
        gray = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY) # Converte a imagem de BGR para escala de cinza.
        gray = cv.equalizeHist(gray) # Equaliza o histograma da imagem em escala de cinza para melhorar o contraste.
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=10, minSize=(30, 30)) # Detecta rostos na imagem.
        for (x, y, w, h) in faces:
            cv.rectangle(self.application, (x, y), (x + w, y + h), (50, 255, 50), 2) # Desenha um retângulo verde ao redor do rosto detectado.
        cv.imshow('FRAME', self.application) # Exibe a imagem em uma janela.
