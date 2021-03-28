clear all;                                  
close all;
%Generación de los bit
N = 10^5+8;
bits = rand(1,N)> 0.5;
%Parametros de la simulacion
%valores discretos sobre los que representamos
EbNodb = 0:10;
EbNo = 10.^(EbNodb/10);
function [bernat,bermap] = qam64mod_sim(bits,EbNo)
    %Modulacion 64QAM
    M=64;
    k = log2(M);
    aux = 0:63;
    simbMod = qammod(aux,64);
    simbModmap = qammod(aux,64,'bin');
    bitsR = reshape(bits',k,[]);
    bitsR = bitsR';
    %modulacion
    simbModulados = zeros(1,size(bitsR,1));
    simbModuladosmap = zeros(1,size(bitsR,1));
    for simb = 1:size(bitsR,1)
        ind = bitsR(simb,:);
        %Pasa a decmal
        pos = bi2de(ind,2,'left-msb')+1;
        simbModulados(simb) = simbMod(pos);
        simbModuladosmap(simb) = simbModmap(pos);
    end
    %Energia simbolo
    Es = mean(abs(simbMod).^2);
    Eb = Es/k;
    % relación entre energía media por bit transmitido y la varianza del ruido
    No = Eb./EbNo;
    %Simulacion
    errores = zeros(1,length(EbNo));
    erroresmap = zeros(1,length(EbNo));
    for i = 1:length(EbNo)
        Noi = No(i);
        %varianza
        var = sqrt(Noi/2);
        %Ruido
        %Distribucion gaussiana media 0
        %varianza No/2
        r_real =  (randn(size(simbModulados)));
        r_imag =  (1j.*randn(size(simbModulados)));
        ruido = var*(r_real + r_imag);
        %Recepcion
        simbRec = simbModulados + ruido;
        simbRecmap = simbModuladosmap + ruido;
        %Demodulacion
        simbEstimated = [];
        simbEstimatedmap = [];
        for x = 1:length(simbRec)
            %calcula de la distancia minima con otros simbolos
            [~,pos] = min(abs(simbRec(x) - simbMod));
            simbEstimated = [simbEstimated,de2bi(pos-1,k,'left-msb')];
            %calcula de la distancia minima con otros simbolos, gray map
            [~,pos] = min(abs(simbRecmap(x) - simbModmap));
            simbEstimatedmap = [simbEstimatedmap,de2bi(pos-1,k,'left-msb')];
        end
        errores(i) = sum(abs(bits-simbEstimated));
        erroresmap(i) = sum(abs(bits-simbEstimatedmap));
    end
    N = length(bits);
    bernat = errores/N;
    bermap = erroresmap/N;
end

