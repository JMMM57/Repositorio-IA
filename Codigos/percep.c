#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#define EPOCAS 300000  
#define K 0.1f          


float W_oculta[2][2]; 
float B_oculta[2];    

float W_salida[2];    
float B_salida;       

float Error_Global = 0.0f;

float sigmoide(float s);
float derivada_sigmoide(float s);
void pesos_init(void);
float EntNt(float x0, float x1, float target);
float Forward(float x0, float x1);

float sigmoide(float s) {
    return 1.0f / (1.0f + expf(-s));
}

float derivada_sigmoide(float out) {
    return out * (1.0f - out);
}

void pesos_init(void) {
    srand((unsigned int)time(NULL));
    
    for (int i = 0; i < 2; i++) {
        B_oculta[i] = ((float)rand() / RAND_MAX) * 2.0f - 1.0f;
        for (int j = 0; j < 2; j++) {
            W_oculta[i][j] = ((float)rand() / RAND_MAX) * 2.0f - 1.0f;
        }
    }
    
    B_salida = ((float)rand() / RAND_MAX) * 2.0f - 1.0f;
    W_salida[0] = ((float)rand() / RAND_MAX) * 2.0f - 1.0f;
    W_salida[1] = ((float)rand() / RAND_MAX) * 2.0f - 1.0f;
}

float EntNt(float x0, float x1, float target) {
    float h_net[2], h_out[2];
    float o_net, o_out;
    
    for (int i = 0; i < 2; i++) {
        h_net[i] = W_oculta[i][0] * x0 + W_oculta[i][1] * x1 + B_oculta[i];
        h_out[i] = sigmoide(h_net[i]);
    }

    o_net = W_salida[0] * h_out[0] + W_salida[1] * h_out[1] + B_salida;
    o_out = sigmoide(o_net);

    float error_salida = target - o_out;
    Error_Global += fabsf(error_salida);

    float delta_salida = error_salida * derivada_sigmoide(o_out);

    float delta_oculta[2];
    for (int i = 0; i < 2; i++) {
        delta_oculta[i] = (delta_salida * W_salida[i]) * derivada_sigmoide(h_out[i]);
    }

    for (int i = 0; i < 2; i++) {
        W_salida[i] += K * delta_salida * h_out[i];
    }
    B_salida += K * delta_salida;

    for (int i = 0; i < 2; i++) {
        W_oculta[i][0] += K * delta_oculta[i] * x0;
        W_oculta[i][1] += K * delta_oculta[i] * x1;
        B_oculta[i]    += K * delta_oculta[i];
    }

    return o_out;
}

float Forward(float x0, float x1) {
    float h_out[2];
    for (int i = 0; i < 2; i++) {
        h_out[i] = sigmoide(W_oculta[i][0] * x0 + W_oculta[i][1] * x1 + B_oculta[i]);
    }
    return sigmoide(W_salida[0] * h_out[0] + W_salida[1] * h_out[1] + B_salida);
}

int main() {
    pesos_init();

    printf("Iniciando Entrenamiento para AND con 2 Capas...\n");

    // Entrenamiento para compuerta AND
    // Entradas: (1,1)->1, (1,0)->0, (0,1)->0, (0,0)->0
    for (int i = 0; i < EPOCAS; i++) {
        Error_Global = 0.0f;
        
        EntNt(1, 1, 1);
        EntNt(1, 0, 0);
        EntNt(0, 1, 0);
        EntNt(0, 0, 0);

        // Imprimir avance cada 20,000 épocas
        if (i % 20000 == 0) {
            printf("Época %d | Error acumulado: %f\n", i, Error_Global);
        }
    }

    printf("\n--- RESULTADOS FINALES EN TREN DE PRUEBA (AND) ---\n");
    printf("1 AND 1 = %f (Esperado: 1)\n", Forward(1, 1));
    printf("1 AND 0 = %f (Esperado: 0)\n", Forward(1, 0));
    printf("0 AND 1 = %f (Esperado: 0)\n", Forward(0, 1));
    printf("0 AND 0 = %f (Esperado: 0)\n", Forward(0, 0));

    return 0;
}