#include <iostream>
#include <iomanip>
#include <cmath>

using namespace std;

struct no {
    int valor;
    struct no *esq;
    struct no *dir;       
};

struct no *raiz;

void iniciaArvore() {
    cout << "\nÁrvore Binária Iniciada!\n";
    raiz = NULL;
}

bool testaArvoreVazia() {
    return (raiz == NULL);
}

int altura(struct no *r) {
    if (r == NULL) return 0;
    return max(altura(r->esq), altura(r->dir)) + 1;
}

bool insereArvore(int num) {
    struct no *pt = new struct no;
    pt->valor = num; 
    pt->esq = NULL;
    pt->dir = NULL;    

    if (testaArvoreVazia()) {
        raiz = pt;
        cout << "Inserido na raiz: " << num << "\n";                    
        return true;
    } 

    if (altura(raiz) >= 5) {
        cout << "Não é possível inserir " << num << ": altura máxima de 5 níveis alcançada.\n";
        delete pt;  // Libera a memória se não for inserido
        return false;
    }

    struct no *b = raiz; 
    while (true) {
        if (num < b->valor) {
            if (b->esq == NULL) {
                b->esq = pt;
                cout << "Inserido à esquerda de " << b->valor << ": " << num << "\n"; 
                return true;
            } else {   
                b = b->esq;
            }
        } else {
            if (b->dir == NULL) {
                b->dir = pt;
                cout << "Inserido à direita de " << b->valor << ": " << num << "\n"; 
                return true;
            } else {   
                b = b->dir;
            }
        }
    }
}

void erd(struct no *r) {
    if (r != NULL) {
        erd(r->esq);
        cout << r->valor << " ";
        erd(r->dir); 
    }
}

void red(struct no *r) {
    if (r != NULL) {
        cout << r->valor << " ";
        red(r->esq);
        red(r->dir); 
    }
}

void edr(struct no *r) {
    if (r != NULL) {
        edr(r->esq);
        edr(r->dir); 
        cout << r->valor << " ";
    }
}

void display(struct no *r, int level, int height) {
    if (r == NULL) return;

    display(r->dir, level + 1, height);
    cout << setw(4 * (height - level)) << r->valor << "\n";
    display(r->esq, level + 1, height);
}

int main() {
    int i, temp;
    iniciaArvore();
    
    // Permitir até 10 tentativas de inserção
    for (i = 0; i < 10; i++) { 
        cout << "Informe um numero: ";
        cin >> temp;
        insereArvore(temp);
    }

    cout << "\nPercurso em Ordem: \n";
    erd(raiz);
    cout << "\nPercurso Pré Ordem: \n";
    red(raiz);
    cout << "\nPercurso Pós Ordem: \n";
    edr(raiz);

    cout << "\n\nVisualização Gráfica da Árvore:\n";
    int h = altura(raiz);
    display(raiz, 0, h);

    return 0;
}
