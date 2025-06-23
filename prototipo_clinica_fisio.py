
from fastapi import FastAPI, Request, Form, WebSocket, Depends
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from datetime import datetime
from reportlab.pdfgen import canvas
import os

app = FastAPI()
os.makedirs("static", exist_ok=True)
templates = Jinja2Templates(directory=".")
app.mount("/static", StaticFiles(directory="static"), name="static")

engine = create_engine("sqlite:///./clinicadb.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Paciente(Base):
    _tablename_ = "pacientes"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String)

class Medico(Base):
    _tablename_ = "medicos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    especialidade = Column(String)

class Consulta(Base):
    _tablename_ = "consultas"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    medico_id = Column(Integer, ForeignKey("medicos.id"))
    data_hora = Column(DateTime)
    descricao = Column(Text)
    paciente = relationship("Paciente")
    medico = relationship("Medico")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def enviar_email(destinatario, assunto, corpo):
    print(f"[EMAIL] Para: {destinatario} | Assunto: {assunto} | Corpo: {corpo}")

def enviar_whatsapp(numero, mensagem):
    print(f"[WHATSAPP] Para: {numero} | Mensagem: {mensagem}")

def gerar_pdf(tipo, paciente_nome):
    caminho = f"static/{tipo}{paciente_nome.replace(' ', '')}.pdf"
    c = canvas.Canvas(caminho)
    if tipo == "boleto":
        c.drawString(100, 750, f"Boleto para: {paciente_nome}")
        c.drawString(100, 730, "Valor: R$200,00")
    else:
        c.drawString(100, 750, f"Nota Fiscal: {paciente_nome}")
        c.drawString(100, 730, "Serviço: Fisioterapia - R$200,00")
    c.save()
    return caminho

@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/pacientes/")
def cadastrar_paciente(nome: str = Form(...), email: str = Form(...), db: Session = Depends(get_db)):
    novo = Paciente(nome=nome, email=email)
    db.add(novo)
    db.commit()
    return {"mensagem": "Paciente cadastrado com sucesso"}

@app.post("/medicos/")
def cadastrar_medico(nome: str = Form(...), especialidade: str = Form(...), db: Session = Depends(get_db)):
    novo = Medico(nome=nome, especialidade=especialidade)
    db.add(novo)
    db.commit()
    return {"mensagem": "Médico cadastrado com sucesso"}

@app.post("/consultas/")
def marcar_consulta(
    paciente_id: int = Form(...),
    medico_id: int = Form(...),
    data_hora: str = Form(...),
    descricao: str = Form(...),
    db: Session = Depends(get_db)
):
    data = datetime.strptime(data_hora, "%Y-%m-%d %H:%M")
    nova = Consulta(paciente_id=paciente_id, medico_id=medico_id, data_hora=data, descricao=descricao)
    db.add(nova)
    db.commit()
    paciente = db.query(Paciente).get(paciente_id)
    enviar_email(paciente.email, "Confirmação de Consulta", f"Sua consulta será em {data}")
    enviar_whatsapp("5511999999999", f"Sua consulta será em {data}")
    return {"mensagem": "Consulta marcada com sucesso"}

@app.get("/consultas/", response_class=HTMLResponse)
def ver_consultas(request: Request, db: Session = Depends(get_db)):
    consultas = db.query(Consulta).all()
    return templates.TemplateResponse("consultas.html", {"request": request, "consultas": consultas})

@app.get("/boleto/{nome}", response_class=FileResponse)
def baixar_boleto(nome: str):
    return FileResponse(gerar_pdf("boleto", nome), media_type="application/pdf")

@app.get("/nf/{nome}", response_class=FileResponse)
def baixar_nf(nome: str):
    return FileResponse(gerar_pdf("nf", nome), media_type="application/pdf")

@app.websocket("/ws/chat")
async def websocket_chat(ws: WebSocket):
    await ws.accept()
    while True:
        msg = await ws.receive_text()
        await ws.send_text(f"Paciente/Medico diz: {msg}")

html_index = """
<!DOCTYPE html>
<html>
<head><title>Clínica Fisioterapia</title></head>
<body>
<h2>Cadastro de Paciente</h2>
<form method="post" action="/pacientes/">
  <input name="nome" placeholder="Nome completo"><br>
  <input name="email" placeholder="Email"><br>
  <button type="submit">Cadastrar</button>
</form>
<h2>Cadastro de Médico</h2>
<form method="post" action="/medicos/">
  <input name="nome" placeholder="Nome do médico"><br>
  <input name="especialidade" placeholder="Especialidade"><br>
  <button type="submit">Cadastrar</button>
</form>
<h2>Marcar Consulta</h2>
<form method="post" action="/consultas/">
  <input name="paciente_id" placeholder="ID do paciente"><br>
  <input name="medico_id" placeholder="ID do médico"><br>
  <input name="data_hora" placeholder="AAAA-MM-DD HH:MM"><br>
  <input name="descricao" placeholder="Descrição"><br>
  <button type="submit">Marcar Consulta</button>
</form>
<a href="/consultas/">Ver Consultas</a><br><br>
<h2>Chat</h2>
<textarea id="chatlog" rows="10" cols="50" readonly></textarea><br>
<input id="msg" placeholder="Mensagem...">
<button onclick="enviar()">Enviar</button>
<script>
  let ws = new WebSocket("ws://localhost:8000/ws/chat");
  ws.onmessage = e => document.getElementById("chatlog").value += e.data + "\\n";
  function enviar() {
    let m = document.getElementById("msg").value;
    ws.send(m);
    document.getElementById("msg").value = "";
  }
</script>
</body>
</html>
"""

html_consultas = """
<!DOCTYPE html>
<html>
<head><title>Consultas</title></head>
<body>
<h2>Consultas Agendadas</h2>
<ul>
{% for c in consultas %}
  <li><b>{{c.data_hora}}</b> - {{c.paciente.nome}} com {{c.medico.nome}} ({{c.descricao}})</li>
{% endfor %}
</ul>
<a href="/">Voltar</a>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_index)

with open("consultas.html", "w", encoding="utf-8") as f:
    f.write(html_consultas)
