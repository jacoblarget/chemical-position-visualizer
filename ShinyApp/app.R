# To run this shinyApp, you will need:
  # The following libraries
  # The following .csv files
  # moleculeViewer.html, sum_xyz.js, and ChemDoodleWebComponents.

# Before running, check to make sure the files are in the right configuration.
  # xyzSummarizer.py,QMdataSummarizer.py,fileList.txt are needed only for the creation of the other files.
  # Concerning the others,
    # |- ShinyApp
    #   |- app.R
    #   |- data
    #       |- sum_anisotropic_constrained_energy.csv
    #       |- sum_anisotropic_unconstrained_energy.csv
    #       |- sum_fullisotropic_constrained_energy.csv
    #       |- sum_fullisotropic_unconstrained_energy.csv
    #       |- sum_index.csv
    #       |- sum_isotropic_constrained_energy.csv
    #       |- sum_isotropic_unconstrained_energy.csv
    #       |- sum_QM_energy.csv
    #       |- sum_scaledispanisotropic_constrained_energy.csv
    #       |- sum_scaledispanisotropic_unconstrained_energy.csv
    #       |- sum_scaledispfullisotropic_constrained_energy.csv
    #       |- sum_scaledispfullisotropic_unconstrained_energy.csv
    #       |- sum_scaledispisotropic_constrained_energy.csv
    #       |- sum_scaledispisotropic_unconstrained_energy.csv
    #   |- www
    #       |-moleculeViewer.html
    #       |-sum_xyz.js
    #       |-ChemDoodleWeb-8.0.0(folder)

# Things left to do:
  # Include the scaledisp... datasets
  # Get rid of unwanted options on the Molecule Viewer's toolbar.
  # ?Highlighting points
  # ?Displaying all data from a certain index when one is clicked
  # ?Other improvements
  # Publish Site

library(shiny)
library(ggplot2)
library(dplyr)
library(shinyjs)

energy = read.csv("data/sum_QM_energy.csv")
indices = read.csv("data/sum_index.csv")
anisotropicunconstrained = read.csv("data/sum_anisotropic_unconstrained_energy.csv")
anisotropicconstrained = read.csv("data/sum_anisotropic_constrained_energy.csv")
fullisotropicunconstrained = read.csv("data/sum_fullisotropic_unconstrained_energy.csv")
fullisotropicconstrained = read.csv("data/sum_fullisotropic_constrained_energy.csv")
isotropicunconstrained = read.csv("data/sum_isotropic_unconstrained_energy.csv")
isotropicconstrained = read.csv("data/sum_isotropic_constrained_energy.csv")

# The following code runs a Javascript function to provide the moleculeViewer.

jsCode = "shinyjs.moleculeViewer = function moleculeViewer(selection){
  display.loadMolecule(moleculeDict[selection]);};"

ui = fluidPage(
   useShinyjs(),
   extendShinyjs(text = jsCode, functions = c("moleculeViewer")),
   title = "Energy Scatterplot",
   fluidRow(
     column(3,
        br(),
        br(),
        selectInput('m1','Molecule 1:',unique(indices$m1)),
        hr(),
        plotOutput("scatterPlot1",
                   dblclick = "plot1_dblclick",
                   click = "plot1_click",
                   brush = brushOpts(
                     id = "plot1_brush",
                     resetOnNew = TRUE
                   )
        ),
        plotOutput("scatterPlot4",
                   dblclick = "plot4_dblclick",
                   click = "plot4_click",
                   brush = brushOpts(
                     id = "plot4_brush",
                     resetOnNew = TRUE
                   )
        )
        
     ),
     column(3,
        h2(textOutput("title")),
        helpText("Highlight and double-click a graph to zoom. Double-click to unzoom. Click on a point to select it."),
        hr(),
        plotOutput("scatterPlot2",
                   dblclick = "plot2_dblclick",
                   click = "plot2_click",
                   brush = brushOpts(
                     id = "plot2_brush",
                     resetOnNew = TRUE
                   )
        ),
        plotOutput("scatterPlot5",
                   dblclick = "plot5_dblclick",
                   click = "plot5_click",
                   brush = brushOpts(
                     id = "plot5_brush",
                     resetOnNew = TRUE
                   )
        )
     ),
     column(3,
        br(),
        br(),
        selectInput('m2', 'Molecule 2:', unique(indices$m2)),
        hr(),
        plotOutput("scatterPlot3",
                   dblclick = "plot3_dblclick",
                   click = "plot3_click",
                   brush = brushOpts(
                     id = "plot3_brush",
                     resetOnNew = TRUE
                   )
        ),
        plotOutput("scatterPlot6",
                   dblclick = "plot6_dblclick",
                   click = "plot6_click",
                   brush = brushOpts(
                     id = "plot6_brush",
                     resetOnNew = TRUE
                   )
        )
     ),
     column(3,
        br(),
        selectInput('c1', 'Dataset:', choices = list("anisotropic", "fullisotropic", "isotropic"),
                    selected = "anisotropic"),
        radioButtons('c2', label = NULL, choices = list("unconstrained" = "unconstrained", "constrained" = "constrained"), 
                     selected = "unconstrained"),
        h4("Selected Point Values"),
        tableOutput("values"),
        hr(),
        h4("Selected Point Molecule Viewer"),
        htmlTemplate("www/moleculeViewer.html")
     )
   )
   )

server = function(input, output, session) {
  
  # This produces the title, which displays the molecules involved in the graph.
  
  output$title = renderText({
    paste(input$m1,"and",input$m2)
  })
  
  # This produces the table that displays the data of a selected point.
  
  output$values = renderTable(digits = 8,{
    selectedPoint()[,c("QM","FF")]
  })
  
  # This is where all six plots graph their respective data frame.
  
  output$scatterPlot1 = renderPlot({
    ggplot(df1(), aes(QM,FF)) +
      geom_point() +
      coord_cartesian(xlim = ranges1$x, ylim = ranges1$y, expand = FALSE) +
      geom_smooth(se=FALSE, method = 'loess') +
      ggtitle("Electrostatics") +
      theme(plot.title = element_text(size = 16, hjust = 0.5))
  })
  output$scatterPlot2 = renderPlot({
    ggplot(df2(), aes(QM,FF)) +
      geom_point() +
      coord_cartesian(xlim = ranges2$x, ylim = ranges2$y, expand = FALSE) +
      geom_smooth(se=FALSE, method = 'loess') +
      ggtitle("Exchange") +
      theme(plot.title = element_text(size = 16, hjust = 0.5))
  })
  output$scatterPlot3 = renderPlot({
    ggplot(df3(), aes(QM,FF)) +
      geom_point() +
      coord_cartesian(xlim = ranges3$x, ylim = ranges3$y, expand = FALSE) +
      geom_smooth(se=FALSE, method = 'loess') +
      ggtitle("Dispersion") +
      theme(plot.title = element_text(size = 16, hjust = 0.5))
  })
  output$scatterPlot4 = renderPlot({
    ggplot(df4(), aes(QM,FF)) +
      geom_point() +
      coord_cartesian(xlim = ranges4$x, ylim = ranges4$y, expand = FALSE) +
      geom_smooth(se=FALSE, method = 'loess') +
      ggtitle("Induction") +
      theme(plot.title = element_text(size = 16, hjust = 0.5))
  })
  output$scatterPlot5 = renderPlot({
    ggplot(df5(), aes(QM,FF)) +
      geom_point() +
      coord_cartesian(xlim = ranges5$x, ylim = ranges5$y, expand = FALSE) +
      geom_smooth(se=FALSE, method = 'loess') +
      ggtitle("δHF") +
      theme(plot.title = element_text(size = 16, hjust = 0.5))
  })
  output$scatterPlot6 = renderPlot({
    ggplot(df6(), aes(QM,FF)) +
      geom_point() +
      coord_cartesian(xlim = ranges6$x, ylim = ranges6$y, expand = FALSE) +
      geom_smooth(se=FALSE, method = 'loess') +
      ggtitle("Total Energy") +
      theme(plot.title = element_text(size = 16, hjust = 0.5))
  })
  
  # These are the reactive data frames, graphed by their respective plots.
  
  df1 = reactive({
    data.frame(QM = energy[getIndices(),"electrostatics"],
               FF = yDataFrame()[getIndices(),"electrostatics"],
               index = yDataFrame()[getIndices(), "index"])
  })
  df2 = reactive({
    data.frame(QM = energy[getIndices(),"exchange"],
               FF = yDataFrame()[getIndices(),"exchange"],
               index = yDataFrame()[getIndices(), "index"])
  })
  df3 = reactive({
    data.frame(QM = energy[getIndices(),"dispersion"],
               FF = yDataFrame()[getIndices(),"dispersion"],
               index = yDataFrame()[getIndices(), "index"])
  })
  df4 = reactive({
    data.frame(QM = energy[getIndices(),"induction"],
               FF = yDataFrame()[getIndices(),"induction"],
               index = yDataFrame()[getIndices(), "index"])
  })
  df5 = reactive({
    data.frame(QM = energy[getIndices(),"dhf"],
               FF = yDataFrame()[getIndices(),"dhf"],
               index = yDataFrame()[getIndices(), "index"])
  })
  df6 = reactive({
    data.frame(QM = energy[getIndices(),"total_energy"],
               FF = yDataFrame()[getIndices(),"total_energy"],
               index = yDataFrame()[getIndices(), "index"])
  })
  
  # The getRow() method returns which row in sum_index.csv contains the range of indices to be graphed.
  
  getRow = reactive({
    return(which( (indices$m1 == input$m1 & indices$m2 == input$m2) | (indices$m1 == input$m2 & indices$m2 == input$m1)))
  })
  
  # The getIndices() method collects all the indices of points to be graphed.
  
  getIndices = reactive({
    c(indices$first[getRow()]:indices$last[getRow()])
  })
  
  # yDataFrame() is a reactive data frame that changes its contents depending on which dataset is selected.
  
  yDataFrame = reactive({
    if(input$c1 == "anisotropic" && input$c2 == "unconstrained")
      anisotropicunconstrained[,c("index","electrostatics","exchange","dispersion","induction","dhf","total_energy")]
    else if(input$c1 == "anisotropic" && input$c2 == "constrained")
      anisotropicconstrained[,c("index","electrostatics","exchange","dispersion","induction","dhf","total_energy")]
    else if(input$c1 == "fullisotropic" && input$c2 == "unconstrained")
      fullisotropicunconstrained[,c("index","electrostatics","exchange","dispersion","induction","dhf","total_energy")]
    else if(input$c1 == "fullisotropic" && input$c2 == "constrained")
      fullisotropicconstrained[,c("index","electrostatics","exchange","dispersion","induction","dhf","total_energy")]
    else if(input$c1 == "isotropic" && input$c2 == "unconstrained")
      isotropicunconstrained[,c("index","electrostatics","exchange","dispersion","induction","dhf","total_energy")]
    else if(input$c1 == "isotropic" && input$c2 == "constrained")
      isotropicconstrained[,c("index","electrostatics","exchange","dispersion","induction","dhf","total_energy")]
  })
  
  # This initializes the selectedGraph$A variable, which starts unselected.
  
  selectedGraph = reactiveValues(A=0)
  
  # These observeEvents() change selectedGraph to tell the program which graph the user is selecting.
  
  observeEvent(input$plot1_click, {
    selectedGraph$A = 1
  })
  observeEvent(input$plot2_click, {
    selectedGraph$A = 2
  })
  observeEvent(input$plot3_click, {
    selectedGraph$A = 3
  })
  observeEvent(input$plot4_click, {
    selectedGraph$A = 4
  })
  observeEvent(input$plot5_click, {
    selectedGraph$A = 5
  })
  observeEvent(input$plot6_click, {
    selectedGraph$A = 6
  })
  
  # Here, the selectedPoint() reactive data frame is set to the point selected by a user.
  
  selectedPoint = reactive({
    if(selectedGraph$A==0){
      nearPoints(df1(), input$plot1_click, maxpoints = 1)
    }
    else if(selectedGraph$A==1){
      nearPoints(df1(), input$plot1_click, maxpoints = 1)
    }
    else if(selectedGraph$A==2){
      nearPoints(df2(), input$plot2_click, maxpoints = 1)
    }
    else if(selectedGraph$A==3){
      nearPoints(df3(), input$plot3_click, maxpoints = 1)
    }
    else if(selectedGraph$A==4){
      nearPoints(df4(), input$plot4_click, maxpoints = 1)
    }
    else if(selectedGraph$A==5){
      nearPoints(df5(), input$plot5_click, maxpoints = 1)
    }
    else if(selectedGraph$A==6){
      nearPoints(df6(), input$plot6_click, maxpoints = 1)
    }
  })
  
  # Here, the selectedIndex() reactive variable is set to the index number of a point clicked by the user.
  
  tol = 10^(-12)
  selectedIndex = reactive({
    if(selectedGraph$A==1){
      df1()$index[abs(df1()$QM-selectedPoint()$QM) < tol & abs(df1()$FF-selectedPoint()$FF) < tol]
    }
    else if(selectedGraph$A==2){
      df2()$index[abs(df2()$QM-selectedPoint()$QM) < tol & abs(df2()$FF-selectedPoint()$FF) < tol]
    }
    else if(selectedGraph$A==3){
      df3()$index[abs(df3()$QM-selectedPoint()$QM) < tol & abs(df3()$FF-selectedPoint()$FF) < tol]
    }
    else if(selectedGraph$A==4){
      df4()$index[abs(df4()$QM-selectedPoint()$QM) < tol & abs(df4()$FF-selectedPoint()$FF) < tol]
    }
    else if(selectedGraph$A==5){
      df5()$index[abs(df5()$QM-selectedPoint()$QM) < tol & abs(df5()$FF-selectedPoint()$FF) < tol]
    }
    else if(selectedGraph$A==6){
      df6()$index[abs(df6()$QM-selectedPoint()$QM) < tol & abs(df6()$FF-selectedPoint()$FF) < tol]
    }
  })
  
  # These ranges and observeEvents() resize their respective graph to a higlighted section.
  
  ranges1 = reactiveValues(x = NULL, y = NULL)
  ranges2 = reactiveValues(x = NULL, y = NULL)
  ranges3 = reactiveValues(x = NULL, y = NULL)
  ranges4 = reactiveValues(x = NULL, y = NULL)
  ranges5 = reactiveValues(x = NULL, y = NULL)
  ranges6 = reactiveValues(x = NULL, y = NULL)
  
  observeEvent(input$plot1_dblclick, {
    brush = input$plot1_brush
    if (!is.null(brush)) {
      ranges1$x = c(brush$xmin, brush$xmax)
      ranges1$y = c(brush$ymin, brush$ymax)
      
    } else {
      ranges1$x = NULL
      ranges1$y = NULL
    }
  })
  observeEvent(input$plot2_dblclick, {
    brush = input$plot2_brush
    if (!is.null(brush)) {
      ranges2$x = c(brush$xmin, brush$xmax)
      ranges2$y = c(brush$ymin, brush$ymax)
      
    } else {
      ranges2$x = NULL
      ranges2$y = NULL
    }
  })
  observeEvent(input$plot3_dblclick, {
    brush = input$plot3_brush
    if (!is.null(brush)) {
      ranges3$x = c(brush$xmin, brush$xmax)
      ranges3$y = c(brush$ymin, brush$ymax)
      
    } else {
      ranges3$x = NULL
      ranges3$y = NULL
    }
  })
  observeEvent(input$plot4_dblclick, {
    brush = input$plot4_brush
    if (!is.null(brush)) {
      ranges4$x = c(brush$xmin, brush$xmax)
      ranges4$y = c(brush$ymin, brush$ymax)
      
    } else {
      ranges4$x = NULL
      ranges4$y = NULL
    }
  })
  observeEvent(input$plot5_dblclick, {
    brush = input$plot5_brush
    if (!is.null(brush)) {
      ranges5$x = c(brush$xmin, brush$xmax)
      ranges5$y = c(brush$ymin, brush$ymax)
      
    } else {
      ranges5$x = NULL
      ranges5$y = NULL
    }
  })
  observeEvent(input$plot6_dblclick, {
    brush = input$plot6_brush
    if (!is.null(brush)) {
      ranges6$x = c(brush$xmin, brush$xmax)
      ranges6$y = c(brush$ymin, brush$ymax)
      
    } else {
      ranges6$x = NULL
      ranges6$y = NULL
    }
  })
  
  # This observeEvent() activates the javaScript function, which creates the interactive molecule viewer.
  
  observeEvent(selectedIndex(), {
    js$moleculeViewer(selectedIndex())
  })
  
}

# Finally, here is where the ui and server are combined to run the complete ShinyApp.

shinyApp(ui, server)