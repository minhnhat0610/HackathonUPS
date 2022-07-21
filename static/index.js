$(document).ready(function(){
    let serverURL = '/validate'
    let form_data = new FormData()
    let pdf_url = './upload'
    $("#submit-btn").on('click',async ()=>{
        serverResponse = await SendDataToServer();
        console.log(JSON.parse(serverResponse))
    })

    $("#file-selection").on("change",function(e){
        selectedFile = $(e.currentTarget).prop('files')[0]
        form_data.append("files",selectedFile)
        console.log($("#file-selection").val().split('\\').pop())
    })

    let showPDF = async () =>{
        try{
            let FileName = $("#file-selection").val().split('\\').pop()
            let PDFHandle = await pdfjsLib.getDocument('https://mozilla.github.io/pdf.js/web/compressed.tracemonkey-pldi-09.pdf')
            let page = await PDFHandle.getPage(1)
            console.log($("#pdf-canvas").width())

            viewportWidth = page.getViewport(1).width
            console.log(viewportWidth)
            let scale = viewportWidth / $("#pdf-canvas").width()
            
            $("#pdf-canvas").height(page.getViewport(1).height)
            let viewport = page.getViewport({scale:scale})

            let render_context = {
                canvasContext: $("#pdf-canvas").get(0).getContext('2d'),
                viewport: viewport
            };

            page.render(render_context)
        }
        catch(e){
            alert(e.message)
        }
    }

    let SendDataToServer = () => {
        return new Promise(function(resolve,reject){
            $.ajax({
                url: serverURL,
                type: 'post',
                data: form_data,
                contentType: false,
                processData: false,
                success: function(data){
                    resolve(data)
                },
                error: function(){
                    reject(error)
                }
            })
        })
    }
})