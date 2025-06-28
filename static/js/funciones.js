
function actualizar() {
    var x = document.getElementsByName("cuadro");
    var lista = '';
    var i = 0;
    var id = '-1';
    var busca = '00';
    var yid = '';
    try {
        for (id in x) {
            y = x[i];
            if (y.className == 'sel') {
                yid = y.attributes.id.value;
                lista = lista + ',' + yid;
            };
            i = i + 1;
        };
    } catch (err) {
        var x = '';
    }

    var itex = document.getElementById("idtexto").value;
    var nombre = document.getElementById("ncaptchag").value;
    var ide = document.getElementById("iscaptchag").value;

    var y = new XMLHttpRequest();
    y.onload = function() {
        document.location.href = '/?pag={{ paginator.number }}';
    };
    y.open('GET', '/actualizar/?id=' + ide + '&nombre=' + nombre + '&texto=' + itex + '&lista=' + lista + '&pag={{ paginator.number }}');
    y.send();




};

function duplicar(nombre) {
    var y = new XMLHttpRequest();
    y.onload = function() {
        $('#prueba12342').html(y.response);
        $('#modificarform').modal('show');
    };
    y.open('GET', '/ver_captcha/?id=' + id + '&pag={{ pag }}&idgrupo={{ idgrupo }}&bloqueado=' + bloqueado);
    y.send();

};

function borrarcaptcha(id, pag) {
    var y = new XMLHttpRequest();
    y.onload = function() {
        document.getElementById("listanombres").innerHTML = y.response;
    };
    y.open('GET', '/borrar_captcha/?id=' + id + '&pag=' + pag);
    y.send();
};

function rejillacaptcha(id) {
    marcar_linea(id);
    var y = new XMLHttpRequest();
    y.onload = function() {
        document.getElementById("rejillacaptcha").innerHTML = y.response;
        marcaseleccionado();
    };

    y.open('GET', '/rejillacaptcha/?id=' + id);
    y.send();

    var zy = new XMLHttpRequest();
    zy.onload = function() {
        document.getElementById("pruebacaptcha").innerHTML = zy.response;
    };

    zy.open('GET', '/captcha/?id=' + id);
    zy.send();
};


function cambiaimagen(nombre, ide) {
    var lista = ['00', '01', '02',
        '10', '11', '12',
        '20', '21', '22'
    ];
    var i = 0;
    var id = '-1';
    var busca = '00';

    for (id in lista) {
        busca = lista[i];
        var y = document.getElementById(busca);
        y.src = '{{ STATIC_URL }}imagenes/captchas/' + nombre + i + '.png?' + new Date().getTime();
        i = i + 1;
    };

    try {
        var x = document.getElementsByName("cuadro");
        i = 0;
        for (id in x) {
            x[i].className = "img";
            i += 1;
        };
    } catch (err) {
        var x = '';
    }


    var iact = document.getElementById(nombre + ide + '1').innerHTML.split(',');
    var i = 0;
    try {
        for (id in iact) {
            busca = iact[i];
            este(busca);
            i = i + 1;
        };
    } catch (err) {
        var i = 0;
    }

    var isel = document.getElementById(nombre + ide + '0').innerHTML;
    var itex = document.getElementById(nombre + ide + '2').innerHTML;

    document.getElementById("idtexto").value = itex;
    document.getElementById("nombrecaptcha").value = nombre;
    document.getElementById("iscaptchag").value = ide;


    var y = new XMLHttpRequest();
    y.onload = function() {
        document.getElementById("prueba").innerHTML = y.response;
    };

    y.open('GET', '/captcha/?id=' + nombre);
    y.send();



};

function selecciona(id) {

    var s = document.getElementById('seleccion');
    var y = document.getElementById(id);
    var lista = s.value;
    if (y.className == "selimg") {
        y.className = "img"

        var pos = lista.indexOf(id);
        if (pos >= 0) {
            lista = lista.replace(id, "");
            lista = lista.replace(",,", ",");
        };
    } else {
        y.className = "selimg";
        lista = lista + id + ',';
    };
    s.value = lista;
};

function menu(url) {
    var y = new XMLHttpRequest();
    var z = document.getElementById(url);
    y.onload = function() {
        document.getElementById("pantalla").innerHTML = y.response;
    };

    y.open('GET', '/' + url + '/');
    y.send();
};

function seccion(id, url, destino) {
    var y = new XMLHttpRequest();
    var z = document.getElementById(url);
    y.onload = function() {
        document.getElementById(destino).innerHTML = y.response;
    };

    y.open('GET', url);
    y.send();
};



function trasladaimagen(id) {
    var x = document.getElementsByName("selecimg");
    var i = 0;
    for (i in x) {
        x[i].className = 'no';
    };
    var x = document.getElementsByName("mcuadro");
    var i = 0;
    for (i in x) {
        if (x[i].id != id) {
            x[i].className = 'img';
        };

    };
    este(id);
    var x = document.getElementsByName("cuadro");
    var z = document.getElementById(id);
    var lista = '';
    var i = 0;
    var id = '-1';
    var busca = '00';
    var yid = '';



    try {
        for (id in x) {
            y = x[i];
            if (y.className == 'sel') {
                y.src = z.src + '?' + new Date().getTime();
            };
            i = i + 1;
        };
    } catch (err) {
        var x = '';
    }
};

function divide(nombre) {
    var y = new XMLHttpRequest();
    y.onload = function() {
        nombre = nombre.split('.')[0];
        cambiaimagen(nombre);
    };
    y.open('GET', '/divide/?nombre=' + nombre + '&pag={{ paginator.number }}');
    y.send();
};

async function importarimagen(idfichero, pag) {
    var nombre = document.getElementById('fileSubmission').value;




    var fd = new FormData();
    var fich = document.getElementById(idfichero);
    fd.append("file", fich.files[0]);
    fd.append("pag", pag);
    var y = new XMLHttpRequest();
    y.onload = function() {
        seccion('pag_im', '/pag_im/?pag=' + pag, 'listaimagenes');
    };
    y.open('POST', '/importar/');
    y.send(fd);
};

function guarda_captcha() {
    var fd = new FormData();

    var lista = [];
    var seleccionados = '';
    
    var id = '-1';
    var busca = '00';
    var imagen = '';

    var i = 0;
    var imagenes = document.getElementsByName("edest");
    while (i < imagenes.length) {
        nodo = imagenes[i];
        imagen = nodo.children[0].src;

        if ( imagen.indexOf('/') >=0 ){
            imagen = imagen.split("/");
            imagen = imagen[imagen.length - 1];
        };

        lista.push(imagen);
        
        if ( nodo.className.indexOf('seleccionada') >= 0){
            seleccionados = seleccionados + nodo.id + ',';
        };
        i+=1;
    };


    var nombre = document.getElementById('guardarnombre').value;
    var idsel = document.getElementById('idcaptcha').value;
    var txt = document.getElementById('idtexto').value;
    var pag = document.getElementById('pag').value;


    fd.append("sel", seleccionados);
    fd.append("nom", nombre);
    fd.append("img", lista);
    fd.append("id", idsel);
    fd.append("txt", txt);
    fd.append("pag", pag);

    var y = new XMLHttpRequest();
    y.onload = function() {
        document.getElementById("listanombres").innerHTML = y.response;
        marcaseleccionado();
        //menu('listanombres','/listanombres/?pag={{ paginator.previous_page_number }}');
    };


    y.open('POST', '/guarda_captcha/');
    y.send(fd);
};

function marcaseleccionado() {
    var x = document.getElementsByName("lineas");
    
    i = 0;
    id = '';
    for (z in x) {
        try {
            if (x[i].className.indexOf('marcado') >= 0) {
                id = x[i].id;
                break;
            };
        } catch {
            id = '';
        };

        i += 1;
    };
    if (id.length > 0) {
        document.getElementById("idcaptcha").value = id;
    };

};

function nuevocaptcha() {
    var fd = new FormData();

    var lista = ['00', '01', '02', '10', '11', '12', '20', '21', '22'];
    var imagenes = ['00', '01', '02', '10', '11', '12', '20', '21', '22'];
    var i = 0;
    var id = '-1';
    var busca = '00';

    for (id in lista) {
        busca = lista[i];
        var y = document.getElementById(busca);
        y.src = '/static/img/exclamation.svg'
        i = i + 1;
    };


    try {
        var x = document.getElementsByName("cuadro");
        i = 0;
        for (id in x) {
            x[i].className == "";
            i += 1;
        };
    } catch (err) {
        var x = '';
    }

    document.getElementById('guardarnombre').value = '';
    document.getElementById('idcaptcha').value = '';
    document.getElementById('idtexto').value = '';
    var id = '';
    var y = new XMLHttpRequest();
    y.onload = function() {
        document.getElementById("listanombres").innerHTML = y.response;
        marcaseleccionado();
    };
    y.open('GET', '/nuevo_captcha/');
    y.send();

};

function marcar_linea(id) {

    try {
        var x = document.getElementsByName("lineas");
        i = 0;
        for (z in x) {
            x[i].className = "";
            i += 1;
        };
    } catch (err) {
        var x = '';

    };
    try {
        var x = document.getElementsByName("botonborrar");
        i = 0;
        for (z in x) {
            x[i].className = ""; //"btn btn-default btn-xs  pull-left";
            i += 1;
        };
    } catch (err) {
        var x = '';

    };

    var y = document.getElementById(id);
    y.className = "marcado";

    var y = document.getElementById('b' + id);
    y.className = "marcado";
};

function mover9() {
    const origen = document.querySelectorAll('.celda-imagenl.seleccionada');
    var destino = document.querySelectorAll('.celda-imagenr.seleccionada');
    var edest = document.getElementsByName("edest");

    if (destino.length == 0) {
        destino = edest;
    };
    
    i = 0;
    j = 0;
    while (i < 9) {
        if (i > (destino.length - 1)) {
            break;
        };
        try {
            idestino = destino[i].children[0];
            idestino.src = origen[j].children[0].src;
        } catch {
            destino = [];
        };
        i += 1;
        j += 1;
        if (j > (origen.length - 1)) {
            j = 0;
        };

    };

};

function enviasel() {
    const seleccionadas = document.querySelectorAll('.celda-imagen.seleccionada');
    var lista = '';
    i = 0;
    while  (i < seleccionadas.length) {
        lista = lista + seleccionadas[i].id.replace('v', '') + ',';
        i = i + 1;
    };
    var fd = new FormData();

    fd.append("serie", document.getElementById("serie").value);
    fd.append("ident", document.getElementById("ident").value);
    fd.append("seleccion", lista);
    
    var y = new XMLHttpRequest();
    y.onload = function() {
        y.response = y.response.replace('\n', '');
        var resultado = '  Aceptado';
         if (y.response.indexOf("Aceptado") >= 0) {
            resultado = '  Aceptado';
        } else {
            resultado = '  Denegado';
        };
        document.getElementById("resultado").value = resultado;
    };
    y.open('POST', '/validar/');
    y.send(fd);
};

function seleccionarImagen(elemento) {
    elemento.classList.toggle('seleccionada');
};