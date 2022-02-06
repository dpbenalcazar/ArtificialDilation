folder = '..\samples\';
arch_excel = '..\samples\segm.csv';

Files = dir([folder,'*.png']);
Nf = length(Files);

%% Read Segmentation

last = num2str(Nf+1);
etiquetas = {'ID','x_pup','y_pup','r_pup','x_iri','y_iri','r_iri'};
IDs = {Files.name}';

if exist(arch_excel, 'file')
    cir_pupi = xlsread(arch_excel, 1, ['B2:D',last]);
    cir_iris = xlsread(arch_excel, 1, ['E2:G',last]);
else
    cir_pupi = zeros(Nf,3);
    cir_iris = zeros(Nf,3);
end

%% Label Pupil and Iris}
% Click with the mouse 4 points in the pupil/iris boundary and the click 4
% points in the iris/sclera boundary

for f = 1:Nf
    arch = [folder, Files(f).name];
    titulo = textoTitulo([Files(f).name]);
    
    img1 = iread(arch);
    
    figure(1);
    imshow(img1);
    colormap(jet(256));
    title(titulo)
    drawnow;
    [X,Y] = ginput(8);
    
    [xp, yp, Rp] = circfit(X(1:4),Y(1:4));   
    [xi, yi, Ri] = circfit(X(5:8),Y(5:8));  
    
    cir_pupi(f,:) = [xp, yp, Rp];
    cir_iris(f,:) = [xi, yi, Ri];
    IDs{f} = Files(f).name;
    
    img2 = insertShape(img1,'circle',[xp, yp, Rp],'LineWidth',5,'Color','blue');
    img2 = insertShape(img2,'circle',[xi, yi, Ri],'LineWidth',5,'Color','red');
    
    figure(2);
    imshow(img2);
    title(titulo)
    drawnow;
end


%% Save segmentation

datos = [cir_pupi, cir_iris];

xlswrite(arch_excel, etiquetas, 1);
xlswrite(arch_excel, IDs,   1, 'A2');
xlswrite(arch_excel, datos, 1, 'B2');

