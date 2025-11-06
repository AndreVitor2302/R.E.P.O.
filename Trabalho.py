import re
import requests
from datetime import datetime
from PyPDF2 import PdfReader
import tkinter as tk
from tkinter import filedialog, messagebox

def extrair_datas_pdf(caminho_pdf):
    try:
        reader = PdfReader(caminho_pdf)
        texto = ""
        for pagina in reader.pages:
            texto += pagina.extract_text() or ""
        
        padrao_data = re.compile(
            r'\b(\d{1,2}\s+de\s+[a-zA-ZçÇãõáéíóúâêôû]+\s+de\s+\d{4})\b|'  
            r'\b(\d{1,2}/\d{1,2}/\d{2,4})\b',                             
            re.IGNORECASE
        )
        
        matches = padrao_data.findall(texto)
        datas = [match[0] or match[1] for match in matches if match[0] or match[1]]
        return datas if datas else ["Nenhuma data encontrada."]
    except Exception as e:
        return [f"Erro ao ler o PDF: {e}"]

def verificar_feriados(datas):
    feriados_por_ano = {}
    meses_pt = {
        'janeiro': 1, 'fevereiro': 2, 'março': 3, 'abril': 4, 'maio': 5, 'junho': 6,
        'julho': 7, 'agosto': 8, 'setembro': 9, 'outubro': 10, 'novembro': 11, 'dezembro': 12
    }
    
    datas_parseadas = []
    anos = set()
    for data_str in datas:
        try:
            if 'de' in data_str.lower():
                partes = re.split(r'\s+de\s+', data_str.lower())
                dia = int(partes[0])
                mes_nome = partes[1].split()[0]  
                ano = int(partes[2])
                mes = meses_pt.get(mes_nome)
                if mes:
                    data_obj = datetime(ano, mes, dia)
                    datas_parseadas.append((data_str, data_obj))
                    anos.add(ano)
            else:
                data_obj = datetime.strptime(data_str, '%d/%m/%Y')
                datas_parseadas.append((data_str, data_obj))
                anos.add(data_obj.year)
        except (ValueError, KeyError):
            continue  
    
    for ano in anos:
        try:
            url = f"https://date.nager.at/api/v3/PublicHolidays/{ano}/BR"
            response = requests.get(url)
            if response.status_code == 200:
                feriados = response.json()
                feriados_por_ano[ano] = {f['date']: f['name'] for f in feriados}
            else:
                feriados_por_ano[ano] = {}
        except requests.RequestException:
            feriados_por_ano[ano] = {}
    
    feriados_encontrados = []
    for data_str, data_obj in datas_parseadas:
        ano = data_obj.year
        data_iso = data_obj.strftime('%Y-%m-%d')
        if data_iso in feriados_por_ano.get(ano, {}):
            nome_feriado = feriados_por_ano[ano][data_iso]
            feriados_encontrados.append(f"📅 {data_str} - {nome_feriado}")
    
    return feriados_encontrados if feriados_encontrados else ["Nenhum feriado encontrado nas datas extraídas."]

def selecionar_pdf():
    caminho_pdf = filedialog.askopenfilename(
        title="Selecione um arquivo PDF",
        filetypes=[("Arquivos PDF", "*.pdf")]
    )
    if caminho_pdf:
        status_label.config(text="Extraindo datas...")
        janela.update()
        datas = extrair_datas_pdf(caminho_pdf)
        if "Erro" in datas[0] or "Nenhuma" in datas[0]:
            resultado_label.config(text="\n".join(datas))
            status_label.config(text="")
            return
        
        status_label.config(text="Verificando feriados...")
        janela.update()
        feriados = verificar_feriados(datas)
        titulo_feriados_label.config(text="Datas Feriados Encontradas:")
        resultado_label.config(text="\n".join(feriados))
        status_label.config(text="Verificação concluída.")

janela = tk.Tk()
janela.title("Extrator de Datas Feriados em PDF")
janela.geometry("500x350")
janela.resizable(False, False)

titulo = tk.Label(janela, text="📘 Extrator de Datas Feriados em PDF", font=("Arial", 14, "bold"))
titulo.pack(pady=10)

botao = tk.Button(janela, text="Selecionar PDF", font=("Arial", 12), command=selecionar_pdf)
botao.pack(pady=10)

status_label = tk.Label(janela, text="", font=("Arial", 10), fg="blue")
status_label.pack(pady=5)

titulo_feriados_label = tk.Label(janela, text="", font=("Arial", 12, "bold"), fg="green")
titulo_feriados_label.pack(pady=5)

resultado_label = tk.Label(janela, text="Nenhum arquivo selecionado.", font=("Arial", 11), wraplength=450, justify="left")
resultado_label.pack(pady=20)

rodape = tk.Label(janela, text="Terceiro commit - Desenvolvido em Python", font=("Arial", 9), fg="gray")
rodape.pack(side="bottom", pady=5)

janela.mainloop()
