#!/usr/bin/env python3

import click

@click.command()
@click.option('--name', prompt='Name', help='{First_Name Last_Name}')
@click.option('--email', prompt='Email', help='email@domain.com')
@click.option('--tel', prompt='Phone Number')
@click.option('--addr', prompt='Address')
@click.option('--zip', prompt='Zip Code')
@click.option('--city', prompt='City')
@click.option('--state', prompt='State')
@click.option('--country', prompt='Country')
@click.option('--c_number', prompt='Credit Card Number')
@click.option('--c_month', prompt='Expiration Month')
@click.option('--c_year', prompt='Expiration Year')
@click.option('--cvv', prompt='CVV')

def get_input(name, email, tel, addr, zip, city, state, country, c_number, c_month, c_year, cvv):
    with open("input.txt", "w") as file:
        file.write("order[bn] {n}\n".format(n=name))
        file.write("order[email] {e}\n".format(e=email))
        file.write("order[tel] {t}\n".format(t=tel))
        file.write("order[billing_address] {a}\n".format(a=addr))
        file.write("order[billing_zip] {z}\n".format(z=zip))
        file.write("order[billing_city] {c}\n".format(c=city))
        file.write("order[billing_state] {s}\n".format(s=state))
        file.write("order[billing_country] {c}\n".format(c=country))
        file.write("riearmxa {c}\n".format(c=c_number))
        file.write("credit_card[month] {c}\n".format(c=c_month))
        file.write("credit_card[year] {c}\n".format(c=c_year))
        file.write("credit_card[meknk] {c}\n".format(c=cvv))

if __name__ == "__main__":
    get_input()
