import re, json, random, datetime, sys
random.seed(7)
src=open(sys.argv[1]).read()
AP="ACOSTA BENITEZ CABRERA DOMINGUEZ ESCOBAR FIGUEROA GIMENEZ HERRERA IBARRA JUAREZ LEDESMA MOLINA NAVARRO OLIVERA PAREDES QUIROGA RAMOS SOSA TOLEDO URQUIZA VILLALBA ZAPATA AGUIRRE BARRIOS CORREA DIAZ FERREYRA GODOY LUNA MEDINA".split()
NO="LUCAS MATIAS NICOLAS ALAN BRIAN DAMIAN EZEQUIEL FACUNDO GONZALO HERNAN IVAN JULIAN LEANDRO MAXIMILIANO NAHUEL OSCAR PABLO RODRIGO SANTIAGO TOMAS WALTER".split()
JZ=["TRIB. JUICIO CONCORDIA","OGA CONCORDIA","OGA CHAJARI","JUZG. FEDERAL","OGA FEDERACION","OGA C. DEL URUGUAY"]
DL=["ROBO AGRAVADO","HURTO","COMERCIO DE ESTUPEFACIENTES","HOMICIDIO","ABUSO SEXUAL","LESIONES","ROBO","AMENAZAS","ENCUBRIMIENTO","TENENCIA DE ARMA"]
T=datetime.date(2026,11,23)
f=lambda d:d.strftime('%d/%m/%Y')
def nm():return random.choice(AP),random.choice(NO)+" "+random.choice(NO)
def dni():return str(random.randint(30,46))+"%06d"%random.randint(0,999999)
P=[];R=[]
for i in range(369):
    a,n=nm();c=random.choice([2,3,4,5,6,8,10,12,15,18,22])
    if i<3: fc=T-datetime.timedelta(days=random.randint(1,20))
    elif i<11: fc=T+datetime.timedelta(days=random.randint(2,29))
    elif i<30: fc=T+datetime.timedelta(days=random.randint(31,90))
    else: fc=T+datetime.timedelta(days=random.randint(120,3600))
    fi=fc-datetime.timedelta(days=365*c)
    P.append([i+1,a,n,dni(),random.choice(JZ),random.choice(DL),c,f(fi),f(fc),f(datetime.date(random.randint(1970,2004),random.randint(1,12),random.randint(1,28))),"%d/%02d"%(random.randint(1000,9999),random.randint(18,26))])
for i in range(69):
    a,n=nm();fi=T-datetime.timedelta(days=random.randint(20,500))
    vp=f(fi+datetime.timedelta(days=730)) if random.random()>.15 else ""
    R.append([i+1,a,n,dni(),random.choice(JZ),random.choice(DL),f(fi),vp,"%d/%02d"%(random.randint(1000,9999),random.randint(24,26)),f(datetime.date(random.randint(1975,2005),3,3))])
out=re.sub(r'var IP=\[\[.*?\]\];','var IP='+json.dumps(P,ensure_ascii=False)+';',src,count=1,flags=re.S)
out=re.sub(r'var IR=\[\[.*?\]\];','var IR='+json.dumps(R,ensure_ascii=False)+';',out,count=1,flags=re.S)
# fixed "today" so day counts stay deterministic; isolated storage key
out=out.replace("var td=new Date()","var td=new Date(2026,10,23)").replace("var SK='up3pro_v1'","var SK='up3promo_demo'")
out=out.replace("— Dir. Pref. Vera Jorge Damián","")
open(sys.argv[2],'w').write(out)
print(len(P),len(R), 'IP' in out)
