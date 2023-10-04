from flet import *
import random
import datetime
import os

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate,Paragraph,Table,TableStyle

now = datetime.datetime.now()
formated_data = now.strftime("%d-%m-%Y")

def main(page):
    page.scroll = "auto"
    page.theme_mode = "light"

    all_food = Column()

    def addToFood(e):
        random_price = random.randint(50,100)
        total_price = random_price * int(con_input.content.controls[4].value)
        all_food.controls.append(
            Container(
                padding=10,
                bgcolor="green200",
                content=Column([
                    Text(con_input.content.controls[3].value,weight="bold"),

                    Text(f"Quantidade Comprada: {con_input.content.controls[4].value}",weight="bold", size=20),

                    Row([
                        Text("Total a Pagar", width="bold"),
                        Text(f"${'{:,.2f}'.format(total_price)}")
                        ], alignment="spaceBetween" )
                ])
            )  
        )
        page.update()

    con_input = Container(
        content=Column([
            TextField(label="Usuário"),
            TextField(label="Endereço"),
            Text("Faça seu Pedido", size=25, weight="bold"),
            TextField(label="Nome Comida"),
            TextField(label="Quantidade da Comida"),
            ElevatedButton("Cadastrar Pedido", on_click=addToFood)
        ])
    )

    def saveMinhaNota(e:FilePickerResultEvent):
        you_file_save_location = e.path

        file_path = f"{you_file_save_location}.pdf"
        doc = SimpleDocTemplate(file_path,pagesizes=letter)

        elements = []

        styles = getSampleStyleSheet()
        elements.append(Paragraph("Recibo de compra", styles['Title']))
        customer_name = con_input.content.controls[0].value
        elements.append(Paragraph(f"Nome: {customer_name}", styles['Normal']))
        elements.append(Paragraph(f"Data Pedido: {formated_data}", styles['Normal']))

        address = con_input.content.controls[1].value
        elements.append(Paragraph(f"Endereço: {address}", styles['Normal']))

        elements.append(Paragraph("Seus pedidos de comida", styles['Heading1']))

        list_order = []
        list_order.append(["Nome Comida","Quantidade","Preço"])

        for i in all_food.controls:
            list_order.append([
                i.content.controls[0].value,
                i.content.controls[1].value.replace('$',"").replace(',',''),
                i.content.controls[2].controls[1].value.replace('$',"").replace(',',''),
            ])

        table = Table(list_order)
        table.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0), colors.grey),
            ("TEXTCOLOR",(0,0),(-1,0), colors.whitesmoke),
            ("ALIGN",(0,0),(-1,0),"CENTER"),
            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
            ("FONTSIZE",(0,0),(-1,0),14),
            ("BOTTOMPADDING",(0,0),(-1,0),12),

            ("BACKGROUND",(0,0),(-1,0), colors.beige),
            ("TEXTCOLOR",(0,0),(-1,0), colors.black),
            ("ALIGN",(0,0),(-1,0),"RIGHT"),
            ("FONTNAME",(0,0),(-1,0),"Helvetica"),
            ("FONTSIZE",(0,0),(-1,0),14),
            ("BOTTOMPADDING",(0,0),(-1,0),8),
        ]))

        elements.append(table)
        grand_total = sum([float(row[2]) for row in list_order[1:]])
        elements.append(Paragraph(f"Valor Total: ${grand_total:.2f}", styles['Heading1']))
        doc.build(elements)

    file_saver = FilePicker(
        on_result=saveMinhaNota
    )

    page.overlay.append(file_saver)


    def buildMeuPedido(e):
        Mdialog = AlertDialog(
            title=Text("Nota dos Pedidos", size=30, weight="bold"),
            content=Column([
               
                Row([
                    Text(f"Cliente: {con_input.content.controls[0].value}", weight="bold", size=25),
                ]),

                Row([
                    Text(f"Data do Pedido: {formated_data}", weight="bold", size=25),
                ]),
               
                Row([
                    Text("Endereço do Cliente", weight="bold"),
                    Text(con_input.content.controls[1].value, weight="bold", size=25),
                ],),
                
                Text("Seus Pedidos", weight="bold", size=25),
                all_food
            ], scroll="auto"),
            actions=[
                # Botão para imprimir recibo
                ElevatedButton("Imprimir Recibo", bgcolor="blue", on_click=lambda e: file_saver.save_file())
            ]
        )

        page.dialog = Mdialog
        Mdialog.open = True
        page.update()

    page.floating_action_button = FloatingActionButton(
        icon="Add",bgcolor="blue",
        on_click=buildMeuPedido
    )

    page.add(
            Column([
                con_input,
                Text("Lista de Pedidos", size=20, weight="bold"),
                all_food
            ])
    )

app(target=main)

