from flet import *
import random
import datetime
import os

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

    def buildMeuPedido(e):
        Mdialog = AlertDialog(
            title=Text("Nota dos Pedidos", size=30, width="bold"),
            content = Column([
                Row([
                    Text(con_input.content.controls[0].value,weight="bold", size=25), 

                     Text(f"Data do Pedido: {formated_data}",weight="bold", size=25), 

                     Text(con_input.content.controls[1].value,weight="bold", size=25), 
                    
                     Row([
                          Text("Endereço do Cliente", weight="bold"),
                           Text(con_input.content.controls[1].value,weight="bold", size=25), 
                     ], alignment="end"),
                     Text("Seus Pedidos", weight="bold",size=25)

                 ])
            ])
        )

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

