const E=function(){var p={defaultValue:null,kind:"LocalArgument",name:"count"},y={defaultValue:null,kind:"LocalArgument",name:"cursor"},F={defaultValue:null,kind:"LocalArgument",name:"extendedView"},k={defaultValue:null,kind:"LocalArgument",name:"name"},S={defaultValue:null,kind:"LocalArgument",name:"savedViewSlug"},f={defaultValue:"",kind:"LocalArgument",name:"search"},v={defaultValue:null,kind:"LocalArgument",name:"view"},r={alias:null,args:null,kind:"ScalarField",name:"colorBy",storageKey:null},t={alias:null,args:null,kind:"ScalarField",name:"colorPool",storageKey:null},d={alias:null,args:null,kind:"ScalarField",name:"multicolorKeypoints",storageKey:null},u={alias:null,args:null,kind:"ScalarField",name:"showSkeletons",storageKey:null},K=[{kind:"Variable",name:"name",variableName:"name"},{kind:"Variable",name:"savedViewSlug",variableName:"savedViewSlug"},{kind:"Variable",name:"view",variableName:"extendedView"}],e={alias:null,args:null,kind:"ScalarField",name:"name",storageKey:null},b={alias:null,args:null,kind:"ScalarField",name:"defaultGroupSlice",storageKey:null},l={alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null},a={alias:null,args:null,kind:"ScalarField",name:"path",storageKey:null},h={alias:null,args:null,kind:"ScalarField",name:"color",storageKey:null},w={alias:null,args:null,kind:"ScalarField",name:"value",storageKey:null},T={alias:null,args:null,concreteType:"ColorScheme",kind:"LinkedField",name:"colorScheme",plural:!1,selections:[l,r,t,d,{alias:null,args:null,kind:"ScalarField",name:"opacity",storageKey:null},u,{alias:null,args:null,concreteType:"CustomizeColor",kind:"LinkedField",name:"fields",plural:!0,selections:[{alias:null,args:null,kind:"ScalarField",name:"colorByAttribute",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"fieldColor",storageKey:null},a,{alias:null,args:null,concreteType:"ValueColor",kind:"LinkedField",name:"valueColors",plural:!0,selections:[h,w],storageKey:null}],storageKey:null}],storageKey:null},L={alias:null,args:null,kind:"ScalarField",name:"colorscale",storageKey:null},V={alias:null,args:null,kind:"ScalarField",name:"plugins",storageKey:null},D={alias:null,args:null,kind:"ScalarField",name:"sidebarMode",storageKey:null},C={alias:null,args:null,kind:"ScalarField",name:"createdAt",storageKey:null},N={alias:null,args:null,kind:"ScalarField",name:"datasetId",storageKey:null},n={alias:null,args:null,kind:"ScalarField",name:"info",storageKey:null},A={alias:null,args:null,kind:"ScalarField",name:"lastLoadedAt",storageKey:null},$={alias:null,args:null,kind:"ScalarField",name:"mediaType",storageKey:null},i={alias:null,args:null,kind:"ScalarField",name:"version",storageKey:null},x={alias:null,args:null,kind:"ScalarField",name:"key",storageKey:null},M={alias:null,args:null,kind:"ScalarField",name:"timestamp",storageKey:null},o={alias:null,args:null,kind:"ScalarField",name:"viewStages",storageKey:null},P={alias:null,args:null,kind:"ScalarField",name:"cls",storageKey:null},B={alias:null,args:null,kind:"ScalarField",name:"type",storageKey:null},Q=[{alias:null,args:null,kind:"ScalarField",name:"target",storageKey:null},w],G={alias:null,args:null,kind:"ScalarField",name:"labels",storageKey:null},I={alias:null,args:null,kind:"ScalarField",name:"edges",storageKey:null},g={alias:null,args:null,kind:"ScalarField",name:"ftype",storageKey:null},m={alias:null,args:null,kind:"ScalarField",name:"subfield",storageKey:null},c={alias:null,args:null,kind:"ScalarField",name:"embeddedDocType",storageKey:null},R={alias:null,args:null,kind:"ScalarField",name:"dbField",storageKey:null},s={alias:null,args:null,kind:"ScalarField",name:"description",storageKey:null},_=[{kind:"Variable",name:"after",variableName:"cursor"},{kind:"Variable",name:"first",variableName:"count"},{kind:"Variable",name:"search",variableName:"search"}],q={kind:"Variable",name:"datasetName",variableName:"name"},z=[a,g,m,c,n,s];return{fragment:{argumentDefinitions:[p,y,F,k,S,f,v],kind:"Fragment",metadata:null,name:"DatasetPageQuery",selections:[{alias:null,args:null,concreteType:"AppConfig",kind:"LinkedField",name:"config",plural:!1,selections:[r,t,d,u],storageKey:null},{alias:null,args:K,concreteType:"Dataset",kind:"LinkedField",name:"dataset",plural:!1,selections:[e,b,{alias:null,args:null,concreteType:"DatasetAppConfig",kind:"LinkedField",name:"appConfig",plural:!1,selections:[T],storageKey:null},{args:null,kind:"FragmentSpread",name:"datasetFragment"}],storageKey:null},{args:null,kind:"FragmentSpread",name:"NavFragment"},{args:null,kind:"FragmentSpread",name:"savedViewsFragment"},{args:null,kind:"FragmentSpread",name:"configFragment"},{args:null,kind:"FragmentSpread",name:"stageDefinitionsFragment"},{args:null,kind:"FragmentSpread",name:"viewSchemaFragment"}],type:"Query",abstractKey:null},kind:"Request",operation:{argumentDefinitions:[f,p,y,S,k,v,F],kind:"Operation",name:"DatasetPageQuery",selections:[{alias:null,args:null,concreteType:"AppConfig",kind:"LinkedField",name:"config",plural:!1,selections:[r,t,d,u,L,{alias:null,args:null,kind:"ScalarField",name:"gridZoom",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"loopVideos",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"notebookHeight",storageKey:null},V,{alias:null,args:null,kind:"ScalarField",name:"showConfidence",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"showIndex",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"showLabel",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"showTooltip",storageKey:null},D,{alias:null,args:null,kind:"ScalarField",name:"theme",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"timezone",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"useFrameNumber",storageKey:null}],storageKey:null},{alias:null,args:K,concreteType:"Dataset",kind:"LinkedField",name:"dataset",plural:!1,selections:[e,b,{alias:null,args:null,concreteType:"DatasetAppConfig",kind:"LinkedField",name:"appConfig",plural:!1,selections:[T,{alias:null,args:null,kind:"ScalarField",name:"gridMediaField",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"mediaFields",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"modalMediaField",storageKey:null},V,D,{alias:null,args:null,concreteType:"SidebarGroup",kind:"LinkedField",name:"sidebarGroups",plural:!0,selections:[{alias:null,args:null,kind:"ScalarField",name:"expanded",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"paths",storageKey:null},e],storageKey:null}],storageKey:null},C,N,{alias:null,args:null,kind:"ScalarField",name:"groupField",storageKey:null},l,n,A,$,i,{alias:null,args:null,concreteType:"BrainRun",kind:"LinkedField",name:"brainMethods",plural:!0,selections:[x,i,M,o,{alias:null,args:null,concreteType:"BrainRunConfig",kind:"LinkedField",name:"config",plural:!1,selections:[P,{alias:null,args:null,kind:"ScalarField",name:"embeddingsField",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"method",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"patchesField",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"supportsPrompts",storageKey:null},B,{alias:null,args:null,kind:"ScalarField",name:"maxK",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"supportsLeastSimilarity",storageKey:null}],storageKey:null}],storageKey:null},{alias:null,args:null,concreteType:"Target",kind:"LinkedField",name:"defaultMaskTargets",plural:!0,selections:Q,storageKey:null},{alias:null,args:null,concreteType:"KeypointSkeleton",kind:"LinkedField",name:"defaultSkeleton",plural:!1,selections:[G,I],storageKey:null},{alias:null,args:null,concreteType:"EvaluationRun",kind:"LinkedField",name:"evaluations",plural:!0,selections:[x,i,M,o,{alias:null,args:null,concreteType:"EvaluationRunConfig",kind:"LinkedField",name:"config",plural:!1,selections:[P,{alias:null,args:null,kind:"ScalarField",name:"predField",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"gtField",storageKey:null}],storageKey:null}],storageKey:null},{alias:null,args:null,concreteType:"Group",kind:"LinkedField",name:"groupMediaTypes",plural:!0,selections:[e,$],storageKey:null},{alias:null,args:null,concreteType:"NamedTargets",kind:"LinkedField",name:"maskTargets",plural:!0,selections:[e,{alias:null,args:null,concreteType:"Target",kind:"LinkedField",name:"targets",plural:!0,selections:Q,storageKey:null}],storageKey:null},{alias:null,args:null,concreteType:"NamedKeypointSkeleton",kind:"LinkedField",name:"skeletons",plural:!0,selections:[e,G,I],storageKey:null},{alias:null,args:null,concreteType:"SampleField",kind:"LinkedField",name:"frameFields",plural:!0,selections:[g,m,c,a,R,s,n],storageKey:null},{alias:null,args:null,concreteType:"SampleField",kind:"LinkedField",name:"sampleFields",plural:!0,selections:[a,g,m,c,R,s,n],storageKey:null},{alias:null,args:[{kind:"Variable",name:"slug",variableName:"savedViewSlug"},{kind:"Variable",name:"view",variableName:"view"}],kind:"ScalarField",name:"stages",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"viewCls",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"viewName",storageKey:null}],storageKey:null},{alias:null,args:_,concreteType:"DatasetStrConnection",kind:"LinkedField",name:"datasets",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"total",storageKey:null},{alias:null,args:null,concreteType:"DatasetStrEdge",kind:"LinkedField",name:"edges",plural:!0,selections:[{alias:null,args:null,kind:"ScalarField",name:"cursor",storageKey:null},{alias:null,args:null,concreteType:"Dataset",kind:"LinkedField",name:"node",plural:!1,selections:[e,l,{alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null}],storageKey:null}],storageKey:null},{alias:null,args:null,concreteType:"DatasetStrPageInfo",kind:"LinkedField",name:"pageInfo",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"endCursor",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"hasNextPage",storageKey:null}],storageKey:null}],storageKey:null},{alias:null,args:_,filters:["search"],handle:"connection",key:"DatasetsList_query_datasets",kind:"LinkedHandle",name:"datasets"},{alias:null,args:null,kind:"ScalarField",name:"context",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"dev",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"doNotTrack",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"uid",storageKey:null},i,{alias:null,args:null,kind:"ScalarField",name:"teamsSubmission",storageKey:null},{alias:null,args:[q],concreteType:"SavedView",kind:"LinkedField",name:"savedViews",plural:!0,selections:[l,N,e,{alias:null,args:null,kind:"ScalarField",name:"slug",storageKey:null},s,h,o,C,{alias:null,args:null,kind:"ScalarField",name:"lastModifiedAt",storageKey:null},A],storageKey:null},L,{alias:null,args:null,concreteType:"StageDefinition",kind:"LinkedField",name:"stageDefinitions",plural:!0,selections:[e,{alias:null,args:null,concreteType:"StageParameter",kind:"LinkedField",name:"params",plural:!0,selections:[e,B,{alias:null,args:null,kind:"ScalarField",name:"default",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"placeholder",storageKey:null}],storageKey:null}],storageKey:null},{alias:null,args:[q,{kind:"Variable",name:"viewStages",variableName:"view"}],concreteType:"SchemaResult",kind:"LinkedField",name:"schemaForViewStages",plural:!1,selections:[{alias:null,args:null,concreteType:"SampleField",kind:"LinkedField",name:"fieldSchema",plural:!0,selections:z,storageKey:null},{alias:null,args:null,concreteType:"SampleField",kind:"LinkedField",name:"frameFieldSchema",plural:!0,selections:z,storageKey:null}],storageKey:null}]},params:{cacheID:"2c277c52e6e3352b1da76a483dc913e6",id:null,metadata:{},name:"DatasetPageQuery",operationKind:"query",text:`query DatasetPageQuery(
  $search: String = ""
  $count: Int
  $cursor: String
  $savedViewSlug: String
  $name: String!
  $view: BSONArray!
  $extendedView: BSONArray
) {
  config {
    colorBy
    colorPool
    multicolorKeypoints
    showSkeletons
  }
  dataset(name: $name, view: $extendedView, savedViewSlug: $savedViewSlug) {
    name
    defaultGroupSlice
    appConfig {
      colorScheme {
        id
        colorBy
        colorPool
        multicolorKeypoints
        opacity
        showSkeletons
        fields {
          colorByAttribute
          fieldColor
          path
          valueColors {
            color
            value
          }
        }
      }
    }
    ...datasetFragment
    id
  }
  ...NavFragment
  ...savedViewsFragment
  ...configFragment
  ...stageDefinitionsFragment
  ...viewSchemaFragment
}

fragment NavDatasets on Query {
  datasets(search: $search, first: $count, after: $cursor) {
    total
    edges {
      cursor
      node {
        name
        id
        __typename
      }
    }
    pageInfo {
      endCursor
      hasNextPage
    }
  }
}

fragment NavFragment on Query {
  ...NavDatasets
  ...NavGA
  teamsSubmission
}

fragment NavGA on Query {
  context
  dev
  doNotTrack
  uid
  version
}

fragment configFragment on Query {
  config {
    colorBy
    colorPool
    colorscale
    gridZoom
    loopVideos
    multicolorKeypoints
    notebookHeight
    plugins
    showConfidence
    showIndex
    showLabel
    showSkeletons
    showTooltip
    sidebarMode
    theme
    timezone
    useFrameNumber
  }
  colorscale
}

fragment datasetAppConfigFragment on DatasetAppConfig {
  gridMediaField
  mediaFields
  modalMediaField
  plugins
  sidebarMode
  colorScheme {
    id
    colorBy
    colorPool
    multicolorKeypoints
    opacity
    showSkeletons
    fields {
      colorByAttribute
      fieldColor
      path
      valueColors {
        color
        value
      }
    }
  }
}

fragment datasetFragment on Dataset {
  createdAt
  datasetId
  groupField
  id
  info
  lastLoadedAt
  mediaType
  name
  version
  appConfig {
    ...datasetAppConfigFragment
  }
  brainMethods {
    key
    version
    timestamp
    viewStages
    config {
      cls
      embeddingsField
      method
      patchesField
      supportsPrompts
      type
      maxK
      supportsLeastSimilarity
    }
  }
  defaultMaskTargets {
    target
    value
  }
  defaultSkeleton {
    labels
    edges
  }
  evaluations {
    key
    version
    timestamp
    viewStages
    config {
      cls
      predField
      gtField
    }
  }
  groupMediaTypes {
    name
    mediaType
  }
  maskTargets {
    name
    targets {
      target
      value
    }
  }
  skeletons {
    name
    labels
    edges
  }
  ...frameFieldsFragment
  ...groupSliceFragment
  ...mediaFieldsFragment
  ...mediaTypeFragment
  ...sampleFieldsFragment
  ...sidebarGroupsFragment
  ...viewFragment
}

fragment frameFieldsFragment on Dataset {
  frameFields {
    ftype
    subfield
    embeddedDocType
    path
    dbField
    description
    info
  }
}

fragment groupSliceFragment on Dataset {
  defaultGroupSlice
}

fragment mediaFieldsFragment on Dataset {
  name
  appConfig {
    gridMediaField
    mediaFields
  }
  sampleFields {
    path
  }
}

fragment mediaTypeFragment on Dataset {
  mediaType
}

fragment sampleFieldsFragment on Dataset {
  sampleFields {
    ftype
    subfield
    embeddedDocType
    path
    dbField
    description
    info
  }
}

fragment savedViewsFragment on Query {
  savedViews(datasetName: $name) {
    id
    datasetId
    name
    slug
    description
    color
    viewStages
    createdAt
    lastModifiedAt
    lastLoadedAt
  }
}

fragment sidebarGroupsFragment on Dataset {
  name
  appConfig {
    sidebarGroups {
      expanded
      paths
      name
    }
  }
  ...frameFieldsFragment
  ...sampleFieldsFragment
}

fragment stageDefinitionsFragment on Query {
  stageDefinitions {
    name
    params {
      name
      type
      default
      placeholder
    }
  }
}

fragment viewFragment on Dataset {
  stages(slug: $savedViewSlug, view: $view)
  viewCls
  viewName
}

fragment viewSchemaFragment on Query {
  schemaForViewStages(datasetName: $name, viewStages: $view) {
    fieldSchema {
      path
      ftype
      subfield
      embeddedDocType
      info
      description
    }
    frameFieldSchema {
      path
      ftype
      subfield
      embeddedDocType
      info
      description
    }
  }
}
`}}}();E.hash="fe59ef05d7082066a5ac296df7a3daab";export{E as default};
