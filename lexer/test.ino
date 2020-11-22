




void loop(int a, int var){
  int led=7;
  if(led>=0)
    a++;
  else
    a--;
  for(int i=0; i<10; i++){
    var += i + 2;
  }
  
}

loop(4);


/*
void loop(int par1,int par2,int par4) {
  digitalWrite(led, HIGH);
}

loop(par1,par2,par4);
*/
