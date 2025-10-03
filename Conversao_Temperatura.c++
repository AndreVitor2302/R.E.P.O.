#include <iostream>

using namespace std;

void convertToCelsius(double temp, char scale){
    if(scale == 'F' || scale == 'f'){
        double celsius = (temp - 32) * 5.0/9.0;  // usar 5.0/9.0 para divisão correta em ponto flutuante
        cout << temp << " Fahrenheit é igual a " << celsius << " Celsius." << endl;
    }
    else if(scale == 'K' || scale == 'k'){  // faltava o operador de comparação '=='
        double celsius = temp - 273.15;
        cout << temp << " Kelvin é igual a " << celsius << " Celsius." << endl;
    }
    else{
        cout << "Escala inválida inserida para conversão para Celsius." << endl;
    }
}

void convertToFahrenheit(double temp, char scale){
    if(scale == 'C' || scale == 'c'){
        double fahrenheit = (temp * 9.0/5.0) + 32;
        cout << temp << " Celsius é igual a " << fahrenheit << " Fahrenheit." << endl;  // corrigido texto
    }
    else if(scale == 'K' || scale == 'k'){  // faltava condição no else if
        double fahrenheit = (temp - 273.15) * 9.0/5.0 + 32;
        cout << temp << " Kelvin é igual a " << fahrenheit << " Fahrenheit." << endl;
    }
    else{
        cout << "Escala inválida inserida para conversão para Fahrenheit." << endl;
    }
}

void convertToKelvin(double temp, char scale){
    if(scale == 'C' || scale == 'c'){
        double kelvin = temp + 273.15;
        cout << temp << " Celsius é igual a " << kelvin << " Kelvin." << endl;
    }
    else if(scale == 'F' || scale == 'f'){
        double kelvin = (temp - 32) * 5.0/9.0 + 273.15;  // corrigida fórmula (antes estava (temp - 12))
        cout << temp << " Fahrenheit é igual a " << kelvin << " Kelvin." << endl;
    }
    else{
        cout << "Escala inválida inserida para conversão para Kelvin." << endl;
    }
}

int main(){
    double temperature;
    char scale;
    char choice;
    
    cout << "Conversão de Temperatura\n";
    cout << "Digite 'c' para Celsius, 'f' para Fahrenheit ou 'k' para Kelvin.\n";
    
    do {
        cout << "\nInsira a escala de temperatura para converter de (C/F/K): ";
        cin >> scale;
        cout << "Insira a temperatura: ";  // corrigido 'count' para 'cout'
        cin >> temperature;
        
        cout << "\nQual escala você gostaria de converter?\n";
        cout << "C - Celsius\nF - Fahrenheit\nK - Kelvin\n";
        char convertTo;
        cin >> convertTo;
        
        if(convertTo == 'C' || convertTo == 'c'){  // corrigido nome da variável
            convertToCelsius(temperature, scale);
        }
        else if(convertTo == 'F' || convertTo == 'f'){
            convertToFahrenheit(temperature, scale);  // corrigido nome da função
        }
        else if(convertTo == 'K' || convertTo == 'k'){
            convertToKelvin(temperature, scale);
        }
        else{
            cout << "Escala de conversão selecionada inválida." << endl;
        }
        
        cout << "\nVocê quer realizar outra conversão? (S/N): ";
        cin >> choice;
    } while (choice == 'S' || choice == 's');  // corrigido condição do loop
    
    cout << "Obrigado por usar o conversor de temperatura!\n";
    return 0;
}
