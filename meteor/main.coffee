@Earthquake = new Mongo.Collection "earthquake"
@TW_Stock = new Mongo.Collection "tw_stock"
@Gas_Price = new Mongo.Collection "gas_price"
@Gas_Predict = new Mongo.Collection "gas_predict"

Router.configure
  layoutTemplate: 'layout'


Meteor.startup ->
  Router.map ->
    @route "index",
      path: "/"
      template: "indexPage"

    @route "earthquake",
      path: "/earthquake/"
      template: "eqPage"
      data: ->
        resData =
          earthquakeMsgs: ->
            Earthquake.find()

    @route "tw_stock",
      path: "/tw_stock/"
      template: "twsPage"
      data: ->
        resData =
          tw_stockMsgs: ->
            TW_Stock.find()

    @route "gas_price",
      path: "/gas_price/"
      template: "gpPage"
      data: ->
        resData =
          gas_priceMsgs: ->
            Gas_Price.find()

    @route "gas_predict",
      path: "/gas_predict/"
      template: "gppPage"
      data: ->
        resData =
          gas_predictMsgs: ->
            Gas_Predict.find()


if Meteor.isServer
  Meteor.publish null, ->
    Earthquake.find()
  Meteor.publish null, ->
    TW_Stock.find()
  Meteor.publish null, ->
    Gas_Price.find()
  Meteor.publish null, ->
    Gas_Predict.find()