MACRO( LEARNBOT_WRAP_ICE )
  # External Slice source paths
  SET (EXTERNAL_SLICE "")
  SET (SLICE_PATH "/opt/learnbot/interfaces;/home/learnbot/interfaces")
  SET (INC_LEARNBOTSLICE_PATH "true" )
  SET (ADDITIONAL_SLICE_INCLUDE_PATH "")

  FOREACH (SPATH ${SLICE_PATH})
     IF( ${RoboComp_INTERFACES_DIR} STREQUAL ${SPATH})
       SET(INC_LEARNBOTSLICE_PATH "false")
     ELSE( ${RoboComp_INTERFACES_DIR} STREQUAL ${SPATH})
			SET(ADDITIONAL_SLICE_INCLUDE_PATH ${ADDITIONAL_SLICE_INCLUDE_PATH} -I${SPATH})
     ENDIF( ${RoboComp_INTERFACES_DIR} STREQUAL ${SPATH})
  ENDFOREACH (SPATH ${SLICE_PATH})

  IF (${INC_LEARNBOTSLICE_PATH} STREQUAL "true")
     SET (SLICE_PATH "${SLICE_PATH};${RoboComp_INTERFACES_DIR}")
  ENDIF(${INC_LEARNBOTSLICE_PATH} STREQUAL "true")

  MESSAGE(STATUS "$SLICE_PATH=\"${SLICE_PATH}\"")

  FOREACH (SPATH ${SLICE_PATH})
    MESSAGE(STATUS "Adding ${SPATH} to the Slice directory set.")
    SET (EXTERNAL_SLICE "${EXTERNAL_SLICE} -I${SPATH} ")
  ENDFOREACH (SPATH)

  FOREACH( input_file ${ARGN} )
    SET (SLICE_FILE_FOUND "false")
  	IF( input_file STREQUAL "Logger" )
  		MESSAGE(STATUS "Compile with LoggerComp support." )
  		ADD_DEFINITIONS(-DCOMPILE_LOGGERCOMP=1)
  	ENDIF( input_file STREQUAL "Logger" )

    FOREACH (SPATH ${SLICE_PATH})
      IF (EXISTS "${SPATH}/${input_file}.ice")
        MESSAGE(STATUS "Adding rule to generate ${input_file}.cpp and ${input_file}.h from ${SPATH}/${input_file}.ice  (${SLICECPP_PATH}slice2cpp)" )
        ADD_CUSTOM_COMMAND (
          OUTPUT ${input_file}.cpp ${input_file}.h
          COMMAND ${SLICECPP_PATH}slice2cpp -I${RoboComp_INTERFACES_DIR} ${ADDITIONAL_SLICE_INCLUDE_PATH} -I. ${SPATH}/${input_file}.ice --output-dir .
          DEPENDS ${SPATH}/${input_file}.ice
          COMMENT "Generating ${input_file}.cpp and ${input_file}.h from ${input_file}.ice"
        )
        SET ( SOURCES ${SOURCES} ./${input_file}.cpp)
        SET ( SLICE_FILE_FOUND "true")
      break ()
      ENDIF (EXISTS "${SPATH}/${input_file}.ice")
    ENDFOREACH (SPATH)

    IF (${SLICE_FILE_FOUND} STREQUAL "false")
      MESSAGE(FATAL_ERROR "${input_file}.ice not found in any of the Slice directories (${SLICE_PATH}).")
#     ELSE (${SLICE_FILE_FOUND} STREQUAL "false")
#       MESSAGE( "${input_file}.ice was found!")
    ENDIF (${SLICE_FILE_FOUND} STREQUAL "false")
  ENDFOREACH( input_file )


ENDMACRO( LEARNBOT_WRAP_ICE )
