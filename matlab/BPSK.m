clear all;                                  
close all;
%Generación de los bit
N = 10^5+8;
bits = rand(1,N)> 0.5;
%Parametros de la simulacion
%valores discretos sobre los que representamos
EbNodb = 0:10;
EbNo = 10.^(EbNodb/10);
function [bernat] = bpskmod_sim(bits,EbNo)
    M = 2;
    k = log2(M);
    bitsR = reshape(bits',k,[]);
    bitsR = bitsR';
    simbMod =  [-1 1];
    %Energia simbolo
    Es = mean(abs(simbMod).^2);
    %Energia promedio
    Eb = Es/k;
    % relación entre energía media por bit transmitido y la varianza del ruido
    No = Eb./EbNo;
    %modulation
    simbModulados = zeros(1,size(bitsR,1));
    for simb = 1:length(bitsR)
        ind = bitsR(simb,:);
        %Pasa a decmal
        pos = bi2de(ind,2,'left-msb')+1;
        simbModulados(simb) = simbMod(pos);
    end
    %Simulacion
    errores = zeros(1,length(EbNo));
    for i = 1:length(EbNo)
        Noi = No(i);
        %varianza
        var = sqrt(Noi/2);
        %Ruido
        %Distribucion gaussiana media 0
        %varianza No/2
        ruido = var*randn(size(simbModulados));
        %Recepcion
        simbRec = simbModulados + ruido;
        %Demodulacion
        %Replicamos las matrices y comparamos
        z = repmat(simbRec,M,1);
        y = repmat(simbMod',size(simbRec));
        %calcula de la distancia minima con otros simbolos
        [~,pos] = min(abs(z - y));
        simbEstimated = de2bi(pos-1',k,'left-msb');
        %total de errores en la iteracion
        simbEstR = reshape(simbEstimated',1,[]);
        errores(i) = sum(abs(bits-simbEstR));
    end
    N = length(bits);
    bernat = errores/N;
end