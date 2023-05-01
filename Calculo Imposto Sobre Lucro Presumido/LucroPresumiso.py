from sys import displayhook
import pandas as pd

# Transformando arquivo em um dataframe
faturamento_df = pd.read_excel(r'C:\Users\jolea\OneDrive\Documentos\GitHub\Calcular_Imposto\Calculo Imposto Sobre Lucro Presumido\Arquivos\Faturamento2022.xlsx')
cabeçalho = faturamento_df.iloc[0]
# Transformando primeira linha no cabeçalho
faturamento_df.columns = cabeçalho
# Excluindo primeira linha
faturamento_df = faturamento_df.drop(0, axis=0) # .drop(indice, linha)
# Convertendo variável da coluna valores para float
faturamento_df['Valor'] = faturamento_df['Valor'].astype(float)

# Lucro Presumido

lucroPres_percentual = float(input('Lucro Presumido(%): '))
# lucroPres_percentual = 0.025  # 2,5%

# Impostos Mensais

iss_icms = float(input('ISS/ICMS(%): '))
# iss_icms = 0.023 # 2,3%
pis = 0.0065 # valor fixo
cofins = 0.03 # valor fixo

# Impostos Trimestrais
irpj = float(input('IRPJ(%): '))
# irpj = 0.15
csll = float(input('CSLL(%): '))
# csll = 0.09

# Função de calculo
def impostos_calcular(valor_mensal, valor_tri):
   lucroPresumido_Men = valor_mensal * lucroPres_percentual
   lucroPresumido_Tri = valor_tri * lucroPres_percentual

   iss_icms_valor = lucroPresumido_Men * iss_icms
   pis_valor = lucroPresumido_Men * pis
   cofins_valor = lucroPresumido_Men * cofins

   if lucroPresumido_Men > 20000:
     irpj_adicional = (lucroPresumido_Men - 20000) * 0.1
     irpj_valor = (lucroPresumido_Tri * irpj) + irpj_adicional
   else :
      irpj_valor = lucroPresumido_Tri * irpj

   csll_valor = lucroPresumido_Tri * csll

   lucroPresumido_Men = f'{lucroPresumido_Men:.2f}'
   lucroPresumido_Tri = f'{lucroPresumido_Tri:.2f}'
   iss_icms_valor = f'{iss_icms_valor:.2f}'
   pis_valor = f'{pis_valor:.2f}'
   cofins_valor = f'{cofins_valor:.2f}'
   irpj_valor = f'{irpj_valor:.2f}'
   csll_valor = f'{csll_valor:.2f}'

   return lucroPresumido_Men, lucroPresumido_Tri, iss_icms_valor, pis_valor, cofins_valor, irpj_valor, csll_valor

# listas para os resultados dos calculos
lucroPresumido_Mensal = []
lucroPresumido_Trimestral = []
iss_icms_aoMes = []
pis_aoMes = []
cofins_aoMes = []
irpj_trimestre = []
csll_trimestre = []

# Pegando valores do df, aplicando calculo e jogando o resultado na lista
# Para valores Mensais
for valor in faturamento_df['Valor']:
   impostoMensal_calculo = impostos_calcular(valor, 0)
   lucroPresumido_Mensal.append(impostoMensal_calculo[0])
   iss_icms_aoMes.append(impostoMensal_calculo[2])
   pis_aoMes.append(impostoMensal_calculo[3])
   cofins_aoMes.append(impostoMensal_calculo[4])

# Separando cada trimestre em uma variável e formatando resultado da soma
trimestre1 = sum(faturamento_df['Valor'][:3])
trimestre2 = sum(faturamento_df['Valor'][3:6])
trimestre3 = sum(faturamento_df['Valor'][6:9])
trimestre4 = sum(faturamento_df['Valor'][9:12])


# lista para os resultados dos trismestres 
trimestre_valores = [trimestre1, trimestre2, trimestre3, trimestre4]


# Pegando valores do df, aplicando calculo e jogando o resultado na lista
# Para valores Trimestrais
for valor in trimestre_valores:
   impostoTri_calculo = impostos_calcular(0, valor)
   lucroPresumido_Trimestral.append(impostoTri_calculo[1])
   irpj_trimestre.append(impostoTri_calculo[5])
   csll_trimestre.append(impostoTri_calculo[6])

# Criando dict para resultados mensais
dic_Mensal = {
   'Meses':  ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'], 'LucroPres Mensal': lucroPresumido_Mensal, 'ISS/ICMS': iss_icms_aoMes, 'Pis': pis_aoMes, 'Cofins': cofins_aoMes
}
# Transformando em df
df_Mensal = pd.DataFrame(dic_Mensal)
displayhook(df_Mensal)

print('-'*100)

# Criando dict para resultados trimestrais
dic_Trimestral = {
   'Trimestres': ['Jan/Fez/Mar', 'Abr/Mai/Jun', 'Jul/Ago/Set', 'Out/Nov/Dez'],'LucroPres Trimestral': lucroPresumido_Trimestral , 'IRPJ': irpj_trimestre , 'CSLL': csll_trimestre
}
# Transformando em df
df_Trimestral = pd.DataFrame(dic_Trimestral)
displayhook(df_Trimestral)